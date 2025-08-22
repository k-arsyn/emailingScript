# 📧 Enhanced Mail Tracker - WhatsApp-Style Read Receipts

A powerful Node.js email tracking system with WhatsApp-like read receipts, perfect for training & placement drives, email campaigns, and bulk email management.

## ✨ Features

### 🎯 WhatsApp-Style Read Receipts

- **✓ Single Tick**: Email delivered successfully
- **✓✓ Double Tick**: Email opened (read)
- **✓✓✓ Triple Tick**: Multiple opens (high engagement)

### 🚀 High-Performance Bulk Operations

- **Ultra-fast bulk creation**: Handle 1000+ emails in seconds
- **Optimized database operations**: Batch transactions for maximum speed
- **Real-time progress indicators**: Professional loading states and progress bars
- **Background Google Sheets sync**: Non-blocking updates

### 📊 Advanced Management

- **Campaign organization**: Group emails by campaigns
- **Search & filtering**: Find emails quickly with advanced search
- **Pagination**: Handle large datasets efficiently
- **Bulk operations**: Select and delete multiple pixels at once

### 📈 Comprehensive Analytics

- **Detailed tracking**: IP addresses, user agents, timestamps
- **Reading patterns**: First read, re-reads, engagement analysis
- **Performance metrics**: Open rates, response times
- **Visual dashboard**: Color-coded status indicators

### 🔗 Google Sheets Integration

- **Automatic updates**: Real-time sync with Google Sheets
- **Campaign tracking**: Organized by campaigns
- **Read receipt status**: Visual indicators in spreadsheet
- **Export-ready data**: Perfect for reports and analysis

## 🔒 Security & Setup

### ⚠️ Important Security Notes

**Before using this application, you MUST configure your own credentials:**

1. **Copy the template configuration:**
   ```bash
   cp config.example.js config.js
   ```

2. **Set up Google Sheets credentials:**
   - Follow the [Google Sheets Setup Guide](GOOGLE_SHEETS_SETUP.md)
   - Download your `google-credentials.json` file
   - **NEVER commit this file to version control**

3. **Configure your settings:**
   - Edit `config.js` with your Google Sheets ID
   - Set environment variables for sensitive data

### Environment Variables

Create a `.env` file (not committed to git):
```bash
GOOGLE_SHEETS_ID=your_spreadsheet_id_here
PORT=3300
```

## 🛠️ Installation

### Prerequisites

- Node.js (v14 or higher)
- Python 3.x (for bulk email sending)

### Quick Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd enhanced-mail-tracker

# Install dependencies
npm install

# Run setup
npm run setup

# Start the application
npm start
```

The application will be available at: http://localhost:3300

## 📋 Usage Guide

### 1. Create a Campaign

1. Open http://localhost:3300
2. Fill in campaign name and description
3. Click "Create Campaign"

### 2. Bulk Email Setup

1. Select your campaign
2. Paste email addresses (one per line)
3. Watch real-time email validation
4. Click "Create Bulk Tracking Pixels"
5. Copy the generated tracking URLs

### 3. Email Integration

Embed tracking pixels in your emails:

```html
<img src="TRACKING_URL" width="1" height="1" style="display:none;" alt="" />
```

### 4. Python Bulk Email Sending

```bash
# Create sample files
npm run python-samples

# Send bulk emails with tracking
python python-email-sender.py \
  --campaign "Training Drive 2024" \
  --emails recipients.csv \
  --template email_template.html \
  --subject "Training & Placement Opportunity" \
  --email your-email@gmail.com \
  --password your-app-password
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```env
PORT=3300
GOOGLE_SHEETS_ID=your-google-sheet-id
```

### Google Sheets Setup (Optional)

1. Follow the guide in `GOOGLE_SHEETS_SETUP.md`
2. Place your credentials in `google-credentials.json`
3. Update the spreadsheet ID in `config.js`

## 📊 Dashboard Features

### Campaign Management

- Create and organize campaigns
- View campaign statistics
- Filter results by campaign

### Email Tracking Results

- **Status Indicators**: Visual read receipt status
- **Search**: Find specific emails or campaigns
- **Pagination**: Navigate through large datasets
- **Bulk Actions**: Select and delete multiple entries

### Advanced Analytics

- **Open Rates**: Campaign performance metrics
- **Reading Patterns**: Engagement analysis
- **Time Tracking**: First read, last read, total opens
- **User Behavior**: IP addresses and user agents

## 🐍 Python Integration

### Features

- **Bulk email sending**: Handle thousands of emails
- **Template support**: HTML email templates with placeholders
- **Progress tracking**: Real-time sending progress
- **Error handling**: Robust error management
- **Rate limiting**: Configurable sending delays

### Email Template Variables

```html
<!-- Use these placeholders in your templates -->
{name}
<!-- Recipient name -->
{email}
<!-- Recipient email -->
{company}
<!-- Company name -->
```

### Supported Email Providers

- Gmail (with App Passwords)
- Outlook/Hotmail
- Yahoo Mail
- Custom SMTP servers

## 📈 Performance

### Optimized for Scale

- **Database**: 500+ pixels/second creation
- **Memory**: Efficient processing without leaks
- **Background Processing**: Non-blocking Google Sheets updates
- **Responsive UI**: Instant feedback with loading states

### Bulk Operations

- **1000 emails**: Created in 2-5 seconds
- **Real-time validation**: Instant email count and duplicate detection
- **Progress tracking**: Visual progress bars and completion status
- **Error resilience**: Continues processing despite individual failures

## 🔒 Privacy & Security

### Invisible Tracking

- 1×1 transparent pixel (completely invisible)
- No recipient notification
- Detailed analytics without user awareness

### Data Protection

- Local SQLite database
- Optional Google Sheets integration
- IP and user agent logging for analysis
- Secure credential handling

### Legal Compliance

- Use responsibly and ethically
- Comply with local privacy laws (GDPR, etc.)
- Consider disclosure requirements
- Respect recipient privacy

## 📁 Project Structure

```
enhanced-mail-tracker/
├── enhanced-tracker.js          # Main application server
├── python-email-sender.py       # Bulk email sending script
├── setup-enhanced-tracker.js    # Setup and initialization
├── config.js                    # Configuration settings
├── package.json                 # Dependencies and scripts
├── views/
│   ├── enhanced-index.ejs       # Main dashboard
│   └── enhanced-logs.ejs        # Detailed analytics
├── services/
│   └── googleSheets.js          # Google Sheets integration
├── public/
│   └── images/
│       └── pixel.png            # 1×1 tracking pixel
└── mail-tracker.db              # SQLite database
```

## 🎯 Use Cases

### Training & Placement Drives

- Track student engagement with placement announcements
- Monitor recruiter interest in job postings
- Identify unopened emails for follow-up
- Measure campaign effectiveness

### Email Marketing

- Newsletter open rates
- Product announcement engagement
- Customer communication tracking
- A/B testing email effectiveness

### Business Communications

- Internal announcement tracking
- Client communication monitoring
- Proposal and document delivery confirmation
- Meeting invitation responses

## 🚀 Getting Started

### Quick Start (5 minutes)

1. **Install**: `npm install && npm run setup`
2. **Start**: `npm start`
3. **Create Campaign**: Go to http://localhost:3300
4. **Add Emails**: Paste your email list
5. **Get URLs**: Copy tracking URLs for your emails

### Advanced Setup (with Google Sheets)

1. Follow `GOOGLE_SHEETS_SETUP.md`
2. Configure credentials
3. Enable automatic spreadsheet updates
4. Export data for analysis

## 📞 Support

### Troubleshooting

- **Database issues**: Run `npm run reset-db`
- **Configuration problems**: Run `npm run check-config`
- **Google Sheets errors**: Check `GOOGLE_SHEETS_SETUP.md`

### Common Issues

- **Port conflicts**: Change PORT in `.env`
- **Email sending failures**: Verify SMTP credentials
- **Large batch timeouts**: Use smaller batches (500-1000 emails)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - Feel free to use for personal and commercial projects.

## 🎉 Acknowledgments

Built for efficient email tracking with professional-grade features and WhatsApp-style user experience.

---

**Ready to track your emails like a pro?** 🚀

Start with: `npm install && npm run setup && npm start`

Then visit: http://localhost:3300
