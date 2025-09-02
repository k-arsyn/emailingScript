#!/usr/bin/env python3
"""
Test script to verify the integrated email tracker loads environment variables correctly
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_credentials():
    print("🔧 Testing integrated email tracker environment setup...")
    
    # SMTP configuration from environment variables
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    sender_email = os.getenv('EMAIL_ADDRESS')
    password = os.getenv('EMAIL_PASSWORD')
    
    # Check if credentials are provided
    if not sender_email or not password:
        print("❌ Error: Email credentials not found!")
        print("Please create a .env file with your email credentials.")
        print("Copy .env.example to .env and fill in your details.")
        return False
    
    # Check if credentials are still placeholders
    if sender_email == 'your_email@gmail.com' or password == 'your_app_password':
        print("⚠️  Warning: Using placeholder credentials!")
        print("Please update your .env file with real credentials before sending emails.")
        return False
    
    print("✅ Environment variables loaded successfully!")
    print(f"📧 Email: {sender_email}")
    print(f"🔒 Password: {'*' * len(password)}")
    print(f"🌐 SMTP Server: {smtp_server}:{smtp_port}")
    
    # Email content
    subject = os.getenv('EMAIL_SUBJECT', 'IIIT Trichy - Placement & Internship Drive 2026')
    print(f"📝 Subject: {subject}")
    
    # Tracking server configuration
    tracking_server = os.getenv('TRACKING_BASE_URL', 'https://emailingscript-production.up.railway.app')
    print(f"📊 Tracking Server: {tracking_server}")
    
    return True

if __name__ == "__main__":
    success = test_credentials()
    if success:
        print("\n✅ Configuration test passed! Ready to send emails.")
    else:
        print("\n❌ Configuration test failed. Please check your .env file.")
