# 📧 Email Tracking System for Bulk Campaigns

A comprehensive email tracking solution with WhatsApp-style read receipts (✓ ✓✓ ✓✓✓) for placement drives and bulk email campaigns.

## 🌟 Features

- **WhatsApp-style Read Receipts**: ✓ Delivered, ✓✓ Read, ✓✓✓ Multiple Opens
- **SVG Tracking Pixels**: Less likely to be cached by email providers
- **Real-time Dashboard**: Monitor email opens in real-time
- **Campaign Management**: Organize emails into campaigns
- **Bulk Email Support**: Send personalized emails to hundreds of recipients
- **Public Hosting Ready**: Deployed on Railway for reliable tracking

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Python Script │───▶│ Node.js Tracker │───▶│   Dashboard     │
│ (Email Sender)  │    │    (Railway)    │    │  (Web UI)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ with pandas, requests
- Node.js 16+ (for local development)
- Gmail account with app password

### 1. Clone Repository
```bash
git clone https://github.com/k-arsyn/emailingScript.git
cd emailingScript
```

### 2. Setup Python Environment
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # Linux/Mac

# Install Python dependencies
pip install -r python-requirements.txt
# Or manually:
# pip install pandas openpyxl requests python-dotenv
```

### 3. Prepare Email Data
- Update `list.xlsx` with company emails
- Update `SpocDetails.xlsx` with SPOC information

### 4. Configure Email Credentials
Edit the email configuration in your Python script:
```python
sender_email = "your-email@gmail.com"
password = "your-app-password"  # Gmail App Password
```

### 5. Send Tracked Emails
```bash
python integrated_email_tracker.py
```

## 📊 Tracking Dashboard

Access the live dashboard at: **https://emailingscript-production.up.railway.app**

### Dashboard Features:
- Campaign overview
- Individual email status
- Read receipt indicators
- Email open timestamps
- Bulk operations

## 🔧 Components

### Core Files

| File | Purpose |
|------|---------|
| `integrated_email_tracker.py` | Main email sender with tracking |
| `bulk-link-generator/` | Node.js tracking service |
| `test_api.py` | API testing script |
| `list.xlsx` | Company email database |
| `SpocDetails.xlsx` | SPOC contact information |

### Tracking Service (`bulk-link-generator/`)
- **Server**: `enhanced-tracker.js`
- **Database**: SQLite (`mail-tracker.db`)
- **Pixel**: `public/images/pixel.svg`
- **Views**: Dashboard templates in `views/`

## 🌐 Deployment

### Current Deployment
- **Platform**: Railway
- **URL**: https://emailingscript-production.up.railway.app
- **Status**: ✅ Active

### Alternative Hosting
For college server deployment (iiitt.ac.in):

1. **Copy tracking service to server**
2. **Install dependencies**: `npm install`
3. **Start service**: `pm2 start enhanced-tracker.js`
4. **Update Python scripts** with new URL

## 📈 Usage Examples

### Basic Campaign
```python
# The script automatically:
# 1. Creates a tracking campaign
# 2. Generates unique SVG pixels for each email
# 3. Sends personalized emails
# 4. Tracks opens in real-time

python integrated_email_tracker.py
```

### API Testing
```python
python test_api.py
```

### Custom Campaign (Advanced)
```python
from integrated_email_tracker import create_campaign_and_get_tracking_urls

campaign_name = "Placement Drive 2026"
tracking_urls = create_campaign_and_get_tracking_urls(campaign_name, email_list)
```

## 🔍 Monitoring

### Read Receipt Status
- **✓ Single tick**: Email delivered (sent)
- **✓✓ Double tick**: Email opened (read)
- **✓✓✓ Triple tick**: Multiple opens (re-read)

### Dashboard Metrics
- Total emails sent
- Open rate percentage
- Campaign performance
- Individual email status

## 🛠️ Troubleshooting

### Common Issues

1. **Gmail Authentication**
   - Use App Password, not regular password
   - Enable 2-factor authentication first

2. **Tracking Not Working**
   - Verify Railway deployment status
   - Check tracking URLs in dashboard

3. **Email Delivery Issues**
   - Check SMTP settings
   - Verify sender email credentials

### Debug Mode
```python
# Add to script for debugging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🔐 Security

- **No sensitive data in repository**
- **Environment variables for credentials**
- **HTTPS tracking URLs**
- **SQLite database (local)**

## 📋 Email Template

The system uses a comprehensive HTML template featuring:
- College branding
- Student statistics with charts
- Participating companies
- Gender distribution
- Contact information
- Tracking pixel (invisible)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create Pull Request

## 📄 License

This project is developed for IIIT Tiruchirappalli placement activities.

## 📞 Support

For issues or questions:
- **Email**: placement@iiitt.ac.in
- **Repository**: [GitHub Issues](https://github.com/k-arsyn/emailingScript/issues)

---

**Made with ❤️ for IIIT Trichy Placement Cell**
