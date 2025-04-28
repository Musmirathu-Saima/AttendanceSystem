from flask import Flask, render_template, request, jsonify
import face_recognition
import cv2
import sqlite3
import pytesseract
import os
import numpy as np
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SAVED_FACES'] = 'saved_faces'

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['SAVED_FACES'], exist_ok=True)

# SQLite Database setup
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  usn TEXT,
                  class_name TEXT,
                  face_encoding BLOB)''')
    conn.commit()
    conn.close()

init_db()

# OCR function
def extract_details(image_path):
    text = pytesseract.image_to_string(image_path)
    lines = text.split('\n')
    name, usn, class_name = '', '', ''

    for line in lines:
        line = line.strip()
        if 'USN' in line.upper():
            usn = line.split()[-1]
        elif 'Class' in line.capitalize():
            class_name = line.split()[-1]
        elif len(line.split()) >= 2 and name == '':
            name = line

    return name, usn, class_name

# Route - Home Page
@app.route('/')
def index():
    return render_template('index.html', name="", usn="", class_name="")

# Route - Upload ID and Extract
@app.route('/upload', methods=['POST'])
def upload():
    id_image = request.files['id_image']
    filename = secure_filename(id_image.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    id_image.save(path)

    # OCR extract
    name, usn, class_name = extract_details(path)

    # Face encode
    id_image_np = face_recognition.load_image_file(path)
    id_face_encodings = face_recognition.face_encodings(id_image_np)

    if len(id_face_encodings) > 0:
        encoding = id_face_encodings[0]

        # Save to DB
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO students (name, usn, class_name, face_encoding) VALUES (?, ?, ?, ?)",
                  (name, usn, class_name, encoding.tobytes()))
        conn.commit()
        conn.close()

        # Save face separately
        np.save(os.path.join(app.config['SAVED_FACES'], usn), encoding)

    return render_template('index.html', name=name, usn=usn, class_name=class_name)

# Route - Verify live capture
@app.route('/verify', methods=['POST'])
def verify():
    live_image = request.files['live_image']
    live_image_np = np.frombuffer(live_image.read(), np.uint8)
    frame = cv2.imdecode(live_image_np, cv2.IMREAD_COLOR)

    # Detect faces
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    if len(face_encodings) == 0:
        return jsonify({'message': '❌ No face detected! Please try again.'})
    elif len(face_encodings) > 1:
        return jsonify({'message': '❌ Invalid: Multiple people detected!'})

    live_encoding = face_encodings[0]

    # Load all encodings from DB
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT name, usn, class_name, face_encoding FROM students")
    students = c.fetchall()
    conn.close()

    for student in students:
        db_name, db_usn, db_class, db_encoding = student
        db_encoding_np = np.frombuffer(db_encoding, dtype=np.float64)

        matches = face_recognition.compare_faces([db_encoding_np], live_encoding)
        if matches[0]:
            return jsonify({'message': f'✅ Verified: {db_name} ({db_usn}) - {db_class}'})

    return jsonify({'message': '❌ Face not recognized!'})

if __name__ == '__main__':
    app.run(debug=True)
