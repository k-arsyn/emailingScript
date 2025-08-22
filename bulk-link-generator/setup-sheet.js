#!/usr/bin/env node

require('dotenv').config();
const { google } = require('googleapis');
const fs = require('fs');
const config = require('./config');

async function setupGoogleSheet() {
  console.log('🔧 Setting up Google Sheet...\n');

  try {
    // Check credentials
    if (!fs.existsSync(config.googleSheets.credentialsPath)) {
      console.log('❌ Google credentials not found. Please add google-credentials.json');
      return;
    }

    if (!config.googleSheets.spreadsheetId) {
      console.log('❌ Spreadsheet ID not configured. Please set GOOGLE_SHEETS_ID in .env');
      return;
    }

    // Load credentials
    const credentials = JSON.parse(fs.readFileSync(config.googleSheets.credentialsPath, 'utf8'));
    
    // Create auth
    const auth = new google.auth.JWT(
      credentials.client_email,
      null,
      credentials.private_key,
      ['https://www.googleapis.com/auth/spreadsheets']
    );

    const sheets = google.sheets({ version: 'v4', auth });

    console.log('✅ Connected to Google Sheets API');

    // Get spreadsheet info
    const spreadsheet = await sheets.spreadsheets.get({
      spreadsheetId: config.googleSheets.spreadsheetId
    });

    console.log(`📊 Spreadsheet: ${spreadsheet.data.properties.title}`);
    console.log('📋 Available sheets:');
    
    spreadsheet.data.sheets.forEach((sheet, index) => {
      console.log(`   ${index + 1}. ${sheet.properties.title}`);
    });

    // Check if our target sheet exists
    const targetSheet = spreadsheet.data.sheets.find(
      sheet => sheet.properties.title === config.googleSheets.sheetName
    );

    if (!targetSheet) {
      console.log(`\n⚠️  Sheet "${config.googleSheets.sheetName}" not found.`);
      console.log('Creating new sheet...');
      
      // Create the sheet
      await sheets.spreadsheets.batchUpdate({
        spreadsheetId: config.googleSheets.spreadsheetId,
        resource: {
          requests: [{
            addSheet: {
              properties: {
                title: config.googleSheets.sheetName
              }
            }
          }]
        }
      });
      
      console.log(`✅ Created sheet: ${config.googleSheets.sheetName}`);
    } else {
      console.log(`✅ Found sheet: ${config.googleSheets.sheetName}`);
    }

    // Set up headers
    console.log('📝 Setting up headers...');
    await sheets.spreadsheets.values.update({
      spreadsheetId: config.googleSheets.spreadsheetId,
      range: `${config.googleSheets.sheetName}!A1:H1`,
      valueInputOption: 'RAW',
      resource: {
        values: [config.googleSheets.headers]
      }
    });

    console.log('✅ Headers configured successfully!');
    console.log('\n🎉 Google Sheets setup complete!');
    console.log('You can now start your application with: npm start');

  } catch (error) {
    console.error('❌ Error setting up Google Sheets:', error.message);
    
    if (error.message.includes('Unable to parse range')) {
      console.log('\n💡 Tip: Make sure your sheet name doesn\'t have special characters');
      console.log('Current sheet name:', config.googleSheets.sheetName);
    }
  }
}

setupGoogleSheet();