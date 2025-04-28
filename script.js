function showSection(section) {
    const content = document.getElementById('content');
    content.style.display = 'block';
  
    let html = '<button class="close-btn" onclick="closeSection()">Close</button>';
  
    switch (section) {
      case 'student':
        html += `
          <h2>Student Interface</h2>
          <ul>
            <li>Mark Attendance</li>
            <li>View Attendance History</li>
            <li>Profile</li>
            <li>Notifications</li>
            <li>Download Attendance Report</li>
          </ul>
        `;
        break;
      case 'teacher':
        html += `
          <h2>Teacher Dashboard</h2>
          <ul>
            <li>Live Attendance Feed</li>
            <li>Generate Reports</li>
            <li>Search & Filter Students</li>
            <li>Train/Update Face Dataset</li>
            <li>Manually Adjust Attendance</li>
            <li>System Settings</li>
          </ul>
        `;
        break;
      case 'admin':
        html += `
          <h2>Admin Panel</h2>
          <ul>
            <li>Manage Users</li>
            <li>View All ATTL Attendance Logs</li>
            <li>View All Attendance Logs</li>
            <li>Generate Reports</li>
            <li>Class Summary</li>
            <li>Permission Controls</li>
          </ul>
        `;
        break;
      case 'analytics':
        html += `
          <h2>Analytics</h2>
          <ul>
            <li>Daily/Weekly/Monthly Graphs</li>
            <li>Pie Charts</li>
            <li>Top Students by Attendance</li>
            <li>Heatmap</li>
          </ul>
          <h3>Optional Smart Add-Ons:</h3>
          <ul>
            <li>Voice Notifications on Successful Attendance</li>
            <li>Camera Feed Preview for Face Detection</li>
            <li>QR Code Attendance (as backup)</li>
            <li>Email Alerts to Parents for Absenteeism</li>
            <li>Mobile App Integration Link (planned)</li>
          </ul>
        `;
        break;
    }
  
    content.innerHTML = html;
  }
  
  function closeSection() {
    const content = document.getElementById('content');
    content.style.display = 'none';
    content.innerHTML = '';
  }