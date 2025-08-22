#!/usr/bin/env node

require('dotenv').config();
const config = require('./config');
const fs = require('fs');

console.log('🔍 Mail Tracker Configuration Check\n');

// Check environment variables
console.log('📋 Environment Variables:');
console.log(`   GOOGLE_SHEETS_ID: ${process.env.GOOGLE_SHEETS_ID ? '✅ Set' : '❌ Not set'}`);
console.log(`   PORT: ${process.env.PORT || 'Using default (3300)'}\n`);

// Check config values
console.log('⚙️  Configuration Values:');
console.log(`   Spreadsheet ID: ${config.googleSheets.spreadsheetId || '❌ Empty'}`);
console.log(`   Sheet Name: ${config.googleSheets.sheetName}`);
console.log(`   Server Port: ${config.server.port}\n`);

// Check credentials file
const credentialsPath = config.googleSheets.credentialsPath;
console.log('🔐 Google Credentials:');
if (fs.existsSync(credentialsPath)) {
  console.log(`   ✅ Credentials file found: ${credentialsPath}`);
  try {
    const creds = JSON.parse(fs.readFileSync(credentialsPath, 'utf8'));
    console.log(`   ✅ Service Account: ${creds.client_email}`);
    console.log(`   ✅ Project ID: ${creds.project_id}`);
  } catch (error) {
    console.log(`   ❌ Invalid JSON in credentials file: ${error.message}`);
  }
} else {
  console.log(`   ❌ Credentials file not found: ${credentialsPath}`);
}

console.log('\n🎯 Next Steps:');
if (!config.googleSheets.spreadsheetId) {
  console.log('   1. Set GOOGLE_SHEETS_ID in your .env file');
  console.log('   2. Make sure there are no spaces around the = sign');
}
if (!fs.existsSync(credentialsPath)) {
  console.log('   1. Download your Google service account credentials');
  console.log('   2. Save as google-credentials.json in the project root');
}
if (config.googleSheets.spreadsheetId && fs.existsSync(credentialsPath)) {
  console.log('   ✅ Configuration looks good! Try starting the app.');
}