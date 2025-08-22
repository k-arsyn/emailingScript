#!/usr/bin/env python3
"""
Enhanced Email Sender with WhatsApp-style Read Receipts
Perfect for Training & Placement Drives

This script integrates with your Node.js mail tracker to provide:
- ✓ Single tick: Email delivered
- ✓✓ Double tick: Email opened (read)  
- ✓✓✓ Triple tick: Multiple opens (re-read)

Usage:
    python python-email-sender.py --campaign "Training Drive 2024" --emails emails.txt
"""

import smtplib
import requests
import json
import argparse
import time
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('email_campaign.log'),
        logging.StreamHandler()
    ]
)

class EmailTracker:
    def __init__(self, tracker_url="http://localhost:3300"):
        self.tracker_url = tracker_url
        self.session = requests.Session()
    
    def create_campaign(self, name, description=""):
        """Create a new campaign in the tracker"""
        try:
            response = self.session.post(f"{self.tracker_url}/create-campaign", 
                                       json={"name": name, "description": description})
            if response.ok:
                data = response.json()
                logging.info(f"✅ Campaign created: {name}")
                return data.get('campaignId')
            else:
                logging.error(f"❌ Failed to create campaign: {response.text}")
                return None
        except Exception as e:
            logging.error(f"❌ Error creating campaign: {e}")
            return None
    
    def create_bulk_pixels(self, campaign_id, campaign_name, emails):
        """Create tracking pixels for bulk emails"""
        try:
            response = self.session.post(f"{self.tracker_url}/create-bulk", 
                                       json={
                                           "campaignId": campaign_id,
                                           "campaignName": campaign_name,
                                           "emails": emails
                                       })
            if response.ok:
                data = response.json()
                logging.info(f"✅ Created {data['created']} tracking pixels")
                return data.get('pixels', [])
            else:
                logging.error(f"❌ Failed to create pixels: {response.text}")
                return []
        except Exception as e:
            logging.error(f"❌ Error creating pixels: {e}")
            return []

class BulkEmailSender:
    def __init__(self, smtp_server, smtp_port, email, password, tracker_url="http://localhost:3300"):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email = email
        self.password = password
        self.tracker = EmailTracker(tracker_url)
        self.sent_count = 0
        self.failed_count = 0       
 
    def load_email_template(self, template_file):
        """Load HTML email template"""
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logging.error(f"❌ Error loading template: {e}")
            return None
    
    def load_recipients(self, file_path):
        """Load recipients from CSV or text file"""
        recipients = []
        try:
            if file_path.endswith('.csv'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        recipients.append({
                            'email': row.get('email', '').strip(),
                            'name': row.get('name', '').strip(),
                            'company': row.get('company', '').strip()
                        })
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        email = line.strip()
                        if email and '@' in email:
                            recipients.append({'email': email, 'name': '', 'company': ''})
            
            logging.info(f"📧 Loaded {len(recipients)} recipients")
            return recipients
        except Exception as e:
            logging.error(f"❌ Error loading recipients: {e}")
            return []
    
    def personalize_email(self, template, recipient, tracking_url):
        """Personalize email content with recipient data and tracking pixel"""
        content = template
        
        # Replace placeholders
        content = content.replace('{name}', recipient.get('name', 'Dear Recipient'))
        content = content.replace('{email}', recipient.get('email', ''))
        content = content.replace('{company}', recipient.get('company', ''))
        
        # Add invisible tracking pixel at the end of the email
        tracking_pixel = f'<img src="{tracking_url}" width="1" height="1" style="display:none;" alt="">'
        
        # Insert tracking pixel before closing body tag
        if '</body>' in content:
            content = content.replace('</body>', f'{tracking_pixel}</body>')
        else:
            content += tracking_pixel
            
        return content
    
    def send_bulk_emails(self, campaign_name, recipients_file, template_file, subject, delay=1):
        """Send bulk emails with tracking"""
        
        # Load recipients and template
        recipients = self.load_recipients(recipients_file)
        template = self.load_email_template(template_file)
        
        if not recipients or not template:
            logging.error("❌ Failed to load recipients or template")
            return False
        
        # Create campaign
        campaign_id = self.tracker.create_campaign(campaign_name, f"Bulk email campaign with {len(recipients)} recipients")
        if not campaign_id:
            logging.error("❌ Failed to create campaign")
            return False
        
        # Create tracking pixels
        email_list = [r['email'] for r in recipients]
        pixels = self.tracker.create_bulk_pixels(campaign_id, campaign_name, email_list)
        
        if not pixels:
            logging.error("❌ Failed to create tracking pixels")
            return False
        
        # Create pixel lookup
        pixel_lookup = {p['email']: p['trackingUrl'] for p in pixels}
        
        # Send emails
        logging.info(f"🚀 Starting bulk email send: {len(recipients)} emails")
        
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            
            for i, recipient in enumerate(recipients, 1):
                try:
                    email_addr = recipient['email']
                    tracking_url = pixel_lookup.get(email_addr, '')
                    
                    if not tracking_url:
                        logging.warning(f"⚠️ No tracking URL for {email_addr}")
                        continue
                    
                    # Create email
                    msg = MIMEMultipart('alternative')
                    msg['From'] = self.email
                    msg['To'] = email_addr
                    msg['Subject'] = subject
                    
                    # Personalize content
                    html_content = self.personalize_email(template, recipient, tracking_url)
                    
                    # Attach HTML content
                    html_part = MIMEText(html_content, 'html')
                    msg.attach(html_part)
                    
                    # Send email
                    server.send_message(msg)
                    self.sent_count += 1
                    
                    logging.info(f"✅ Sent {i}/{len(recipients)}: {email_addr}")
                    
                    # Rate limiting
                    if delay > 0:
                        time.sleep(delay)
                        
                except Exception as e:
                    self.failed_count += 1
                    logging.error(f"❌ Failed to send to {recipient.get('email', 'unknown')}: {e}")
                    continue
            
            server.quit()
            logging.info(f"🎉 Campaign completed! Sent: {self.sent_count}, Failed: {self.failed_count}")
            return True
            
        except Exception as e:
            logging.error(f"❌ SMTP Error: {e}")
            return False

def create_sample_files():
    """Create sample template and recipient files"""
    
    # Sample HTML template
    template_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Training & Placement Opportunity</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #4CAF50; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; background: #f9f9f9; }
        .footer { padding: 20px; text-align: center; color: #666; }
        .btn { background: #2196F3; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎓 Training & Placement Opportunity</h1>
        </div>
        <div class="content">
            <p>Hello {name},</p>
            
            <p>We are excited to invite you to our upcoming Training & Placement Drive!</p>
            
            <h3>📅 Event Details:</h3>
            <ul>
                <li><strong>Date:</strong> March 15-16, 2024</li>
                <li><strong>Time:</strong> 9:00 AM - 5:00 PM</li>
                <li><strong>Venue:</strong> Main Auditorium</li>
                <li><strong>Mode:</strong> Hybrid (In-person + Virtual)</li>
            </ul>
            
            <h3>🏢 Participating Companies:</h3>
            <ul>
                <li>TechCorp Solutions</li>
                <li>InnovateTech Ltd</li>
                <li>FutureSoft Systems</li>
                <li>DataDriven Analytics</li>
            </ul>
            
            <h3>💼 Available Positions:</h3>
            <ul>
                <li>Software Developer</li>
                <li>Data Analyst</li>
                <li>System Administrator</li>
                <li>Project Manager</li>
            </ul>
            
            <p>This is a fantastic opportunity to kickstart your career with leading companies in the industry.</p>
            
            <p style="text-align: center;">
                <a href="#" class="btn">Register Now</a>
            </p>
            
            <p>For any queries, please contact us at placement@college.edu</p>
            
            <p>Best regards,<br>
            Placement Cell<br>
            Your College Name</p>
        </div>
        <div class="footer">
            <p>© 2024 College Placement Cell. All rights reserved.</p>
            <p>You received this email because you're registered for placement activities.</p>
        </div>
    </div>
</body>
</html>"""
    
    with open('email_template.html', 'w', encoding='utf-8') as f:
        f.write(template_content)
    
    # Sample recipients CSV
    recipients_csv = """email,name,company
student1@example.com,John Doe,TechCorp
student2@example.com,Jane Smith,InnovateTech
student3@example.com,Mike Johnson,FutureSoft
recruiter1@company.com,Sarah Wilson,DataDriven
recruiter2@company.com,David Brown,TechCorp"""
    
    with open('recipients.csv', 'w', encoding='utf-8') as f:
        f.write(recipients_csv)
    
    # Sample recipients text file
    recipients_txt = """student1@example.com
student2@example.com
student3@example.com
recruiter1@company.com
recruiter2@company.com"""
    
    with open('recipients.txt', 'w', encoding='utf-8') as f:
        f.write(recipients_txt)
    
    print("✅ Sample files created:")
    print("  - email_template.html (HTML email template)")
    print("  - recipients.csv (CSV with name, email, company)")
    print("  - recipients.txt (Simple email list)")

def main():
    parser = argparse.ArgumentParser(description='Send bulk emails with WhatsApp-style read receipts')
    parser.add_argument('--campaign', required=True, help='Campaign name')
    parser.add_argument('--emails', required=True, help='Recipients file (CSV or TXT)')
    parser.add_argument('--template', required=True, help='HTML email template file')
    parser.add_argument('--subject', required=True, help='Email subject')
    parser.add_argument('--smtp-server', default='smtp.gmail.com', help='SMTP server')
    parser.add_argument('--smtp-port', type=int, default=587, help='SMTP port')
    parser.add_argument('--email', required=True, help='Sender email')
    parser.add_argument('--password', required=True, help='Sender password/app password')
    parser.add_argument('--delay', type=float, default=1.0, help='Delay between emails (seconds)')
    parser.add_argument('--tracker-url', default='http://localhost:3300', help='Mail tracker URL')
    parser.add_argument('--create-samples', action='store_true', help='Create sample template and recipient files')
    
    args = parser.parse_args()
    
    if args.create_samples:
        create_sample_files()
        return
    
    # Initialize sender
    sender = BulkEmailSender(
        smtp_server=args.smtp_server,
        smtp_port=args.smtp_port,
        email=args.email,
        password=args.password,
        tracker_url=args.tracker_url
    )
    
    # Send emails
    success = sender.send_bulk_emails(
        campaign_name=args.campaign,
        recipients_file=args.emails,
        template_file=args.template,
        subject=args.subject,
        delay=args.delay
    )
    
    if success:
        print(f"\n🎉 Campaign '{args.campaign}' completed successfully!")
        print(f"📊 Check your tracker dashboard at: {args.tracker_url}")
        print(f"📈 Sent: {sender.sent_count}, Failed: {sender.failed_count}")
    else:
        print("\n❌ Campaign failed. Check the logs for details.")

if __name__ == "__main__":
    main()