// config.js - Configuration for Google Sheets integration
module.exports = {
  // Google Sheets configuration
  googleSheets: {
    // You'll need to create a service account and download the JSON key file
    // Place it in the root directory as 'google-credentials.json'
    credentialsPath: './google-credentials.json',
    

    spreadsheetId: process.env.GOOGLE_SHEETS_ID || '',
    
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