// config.example.js - Template configuration for Google Sheets integration
// Copy this file to config.js and modify with your own settings

module.exports = {
  // Google Sheets configuration
  googleSheets: {
    // You'll need to create a service account and download the JSON key file
    // Place it in the root directory as 'google-credentials.json'
    credentialsPath: './google-credentials.json',
    
    // Your Google Sheets ID (found in the URL)
    // Example: https://docs.google.com/spreadsheets/d/YOUR_SPREADSHEET_ID/edit
    spreadsheetId: process.env.GOOGLE_SHEETS_ID || 'YOUR_SPREADSHEET_ID_HERE',
    
    // The sheet name/tab where data will be written
    sheetName: 'MailTracking',
    
    // Column headers for the sheet
    headers: [
      'Campaign',
      'Recipient Email',
      'Read Receipt',
      'Status',
      'First Opened',
      'Last Opened',
      'Open Count',
      'Created Date',
      'Pixel ID'
    ]
  },
  
  // Server configuration
  server: {
    port: process.env.PORT || 3300
  }
};
