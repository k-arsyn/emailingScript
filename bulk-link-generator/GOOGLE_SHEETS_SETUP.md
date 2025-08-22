# Google Sheets Integration Setup

This guide will help you set up automatic Google Sheets updates for your mail tracking application.

## Step 1: Create a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Sheets API:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Sheets API"
   - Click on it and press "Enable"

## Step 2: Create a Service Account

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "Service Account"
3. Fill in the service account details:
   - Name: `mail-tracker-service`
   - Description: `Service account for mail tracking app`
4. Click "Create and Continue"
5. Skip the optional steps and click "Done"

## Step 3: Generate and Download Credentials

1. In the Credentials page, find your service account
2. Click on the service account email
3. Go to the "Keys" tab
4. Click "Add Key" > "Create New Key"
5. Choose "JSON" format
6. Download the file and rename it to `google-credentials.json`
7. Place this file in your project root directory

## Step 4: Create Your Google Sheet

1. Go to [Google Sheets](https://sheets.google.com)
2. Create a new spreadsheet
3. Name it something like "Mail Tracking Data"
4. Copy the spreadsheet ID from the URL:
   - URL: `https://docs.google.com/spreadsheets/d/1ABC123DEF456.../edit`
   - ID: `1ABC123DEF456...`

## Step 5: Share the Sheet with Service Account

1. In your Google Sheet, click "Share"
2. Add the service account email (found in your `google-credentials.json` file)
3. Give it "Editor" permissions
4. Click "Send"

## Step 6: Configure the Application

1. Open `config.js` in your project
2. Update the `spreadsheetId` with your sheet ID:
   ```javascript
   spreadsheetId: '1ABC123DEF456...' // Your actual sheet ID
   ```

Alternatively, set the environment variable:
```bash
export GOOGLE_SHEETS_ID="1ABC123DEF456..."
```

## Step 7: Test the Integration

1. Install dependencies: `npm install`
2. Start your application: `npm start`
3. Create a new tracking pixel
4. Check your Google Sheet - it should automatically create headers and add the pixel data

## Sheet Structure

The application will automatically create these columns in your sheet:

| Column | Description |
|--------|-------------|
| Pixel Name | Name you gave to the tracking pixel |
| Recipient Email | Email address of the recipient |
| Status | "Seen" or "Unseen" |
| First Opened | Date/time of first email open |
| Last Opened | Date/time of most recent open |
| Open Count | Total number of times opened |
| Created Date | When the pixel was created |
| Pixel ID | Unique identifier for the pixel |

## Troubleshooting

### "Credentials not found" error
- Make sure `google-credentials.json` is in your project root
- Check that the file is valid JSON

### "Permission denied" error
- Ensure you shared the sheet with the service account email
- Verify the service account has "Editor" permissions

### "Sheet not found" error
- Double-check your spreadsheet ID in `config.js`
- Make sure the sheet name matches (default: "Mail Tracking")

### Data not updating
- Check the console for error messages
- Verify your internet connection
- Ensure the Google Sheets API is enabled in your Google Cloud project

## Security Notes

- Keep your `google-credentials.json` file secure and never commit it to version control
- Add `google-credentials.json` to your `.gitignore` file
- The service account only has access to sheets you explicitly share with it
- Consider using environment variables for production deployments