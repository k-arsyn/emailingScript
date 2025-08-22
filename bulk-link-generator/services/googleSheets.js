// services/googleSheets.js - Google Sheets integration service
const { google } = require('googleapis');
const fs = require('fs');
const path = require('path');
const config = require('../config');

class GoogleSheetsService {
  constructor() {
    this.sheets = null;
    this.auth = null;
    this.initialized = false;
  }

  async initialize() {
    try {
      // Check if credentials file exists
      const credentialsPath = path.join(__dirname, '..', config.googleSheets.credentialsPath);
      if (!fs.existsSync(credentialsPath)) {
        console.log('Google Sheets credentials not found. Sheets integration disabled.');
        return false;
      }

      // Load credentials
      const credentials = JSON.parse(fs.readFileSync(credentialsPath, 'utf8'));
      
      // Create JWT auth
      this.auth = new google.auth.JWT(
        credentials.client_email,
        null,
        credentials.private_key,
        ['https://www.googleapis.com/auth/spreadsheets']
      );

      // Initialize sheets API
      this.sheets = google.sheets({ version: 'v4', auth: this.auth });
      
      // Test the connection and setup headers if needed
      await this.setupSheet();
      
      this.initialized = true;
      console.log('Google Sheets integration initialized successfully');
      return true;
    } catch (error) {
      console.error('Failed to initialize Google Sheets:', error.message);
      return false;
    }
  }

  async setupSheet() {
    if (!this.sheets || !config.googleSheets.spreadsheetId) {
      console.log('Google Sheets spreadsheet ID not configured, skipping sheet setup');
      return;
    }

    try {
      // Check if sheet exists and has headers
      const response = await this.sheets.spreadsheets.values.get({
        spreadsheetId: config.googleSheets.spreadsheetId,
        range: `${config.googleSheets.sheetName}!A1:I1`,
      });

      // If no data or headers don't match, set up headers
      if (!response.data.values || response.data.values.length === 0) {
        await this.sheets.spreadsheets.values.update({
          spreadsheetId: config.googleSheets.spreadsheetId,
          range: `${config.googleSheets.sheetName}!A1:I1`,
          valueInputOption: 'RAW',
          resource: {
            values: [config.googleSheets.headers]
          }
        });
        console.log('Sheet headers initialized');
      }
    } catch (error) {
      console.error('Error setting up sheet:', error.message);
    }
  }

  async updatePixelData(pixelData) {
    if (!this.initialized || !this.sheets || !config.googleSheets.spreadsheetId) {
      console.log('Google Sheets not configured or initialized, skipping update');
      return;
    }

    try {
      // Find existing row or create new one
      const existingRowIndex = await this.findPixelRow(pixelData.pixelId);
      
      const rowData = [
        pixelData.campaignName || 'Individual',
        pixelData.recipientEmail || 'Unknown',
        pixelData.readReceipt || pixelData.status, // WhatsApp-style read receipt
        pixelData.status, // 'Seen' or 'Unseen'
        pixelData.firstOpened || '',
        pixelData.lastOpened || '',
        pixelData.openCount || 0,
        pixelData.createdDate,
        pixelData.pixelId
      ];

      if (existingRowIndex > 0) {
        // Update existing row
        await this.sheets.spreadsheets.values.update({
          spreadsheetId: config.googleSheets.spreadsheetId,
          range: `${config.googleSheets.sheetName}!A${existingRowIndex}:I${existingRowIndex}`,
          valueInputOption: 'RAW',
          resource: {
            values: [rowData]
          }
        });
        console.log(`Updated row ${existingRowIndex} for pixel ${pixelData.name}`);
      } else {
        // Append new row
        await this.sheets.spreadsheets.values.append({
          spreadsheetId: config.googleSheets.spreadsheetId,
          range: `${config.googleSheets.sheetName}!A:I`,
          valueInputOption: 'RAW',
          insertDataOption: 'INSERT_ROWS',
          resource: {
            values: [rowData]
          }
        });
        console.log(`Added new row for pixel ${pixelData.name}`);
      }
    } catch (error) {
      console.error('Error updating Google Sheets:', error.message);
    }
  }

  async findPixelRow(pixelId) {
    if (!config.googleSheets.spreadsheetId) {
      return -1;
    }
    
    try {
      const response = await this.sheets.spreadsheets.values.get({
        spreadsheetId: config.googleSheets.spreadsheetId,
        range: `${config.googleSheets.sheetName}!I:I`, // Pixel ID column
      });

      if (response.data.values) {
        for (let i = 0; i < response.data.values.length; i++) {
          if (response.data.values[i][0] === pixelId) {
            return i + 1; // Return 1-based row index
          }
        }
      }
      return -1; // Not found
    } catch (error) {
      console.error('Error finding pixel row:', error.message);
      return -1;
    }
  }

  async deletePixelData(pixelId) {
    if (!this.initialized || !this.sheets || !config.googleSheets.spreadsheetId) {
      console.log('Google Sheets not configured or initialized, skipping delete');
      return;
    }

    try {
      const rowIndex = await this.findPixelRow(pixelId);
      
      if (rowIndex > 1) { // Don't delete header row
        // Use batch update for faster operation - clear and delete in one call
        await this.sheets.spreadsheets.batchUpdate({
          spreadsheetId: config.googleSheets.spreadsheetId,
          resource: {
            requests: [
              {
                // Clear the row data first
                updateCells: {
                  range: {
                    sheetId: 0,
                    startRowIndex: rowIndex - 1,
                    endRowIndex: rowIndex,
                    startColumnIndex: 0,
                    endColumnIndex: 9
                  },
                  fields: 'userEnteredValue'
                }
              },
              {
                // Then delete the row
                deleteDimension: {
                  range: {
                    sheetId: 0,
                    dimension: 'ROWS',
                    startIndex: rowIndex - 1,
                    endIndex: rowIndex
                  }
                }
              }
            ]
          }
        });
        
        console.log(`Deleted row ${rowIndex} for pixel ${pixelId} from Google Sheets`);
      }
    } catch (error) {
      console.error('Error deleting from Google Sheets:', error.message);
      // Don't throw error to avoid blocking the main delete operation
    }
  }

  // Batch delete multiple pixels for better performance
  async deleteBulkPixelData(pixelIds) {
    if (!this.initialized || !this.sheets || !config.googleSheets.spreadsheetId) {
      console.log('Google Sheets not configured or initialized, skipping bulk delete');
      return;
    }

    try {
      const requests = [];
      
      // Find all rows to delete (in reverse order to avoid index shifting)
      const rowsToDelete = [];
      for (const pixelId of pixelIds) {
        const rowIndex = await this.findPixelRow(pixelId);
        if (rowIndex > 1) {
          rowsToDelete.push(rowIndex);
        }
      }
      
      // Sort in descending order to delete from bottom to top
      rowsToDelete.sort((a, b) => b - a);
      
      // Create delete requests
      for (const rowIndex of rowsToDelete) {
        requests.push({
          deleteDimension: {
            range: {
              sheetId: 0,
              dimension: 'ROWS',
              startIndex: rowIndex - 1,
              endIndex: rowIndex
            }
          }
        });
      }
      
      if (requests.length > 0) {
        await this.sheets.spreadsheets.batchUpdate({
          spreadsheetId: config.googleSheets.spreadsheetId,
          resource: { requests }
        });
        
        console.log(`Bulk deleted ${requests.length} rows from Google Sheets`);
      }
    } catch (error) {
      console.error('Error bulk deleting from Google Sheets:', error.message);
      // Don't throw error to avoid blocking the main delete operation
    }
  }
}

module.exports = new GoogleSheetsService();