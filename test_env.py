#!/usr/bin/env python3
"""Test script to verify environment variable loading"""

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Test loading each variable
email_address = os.getenv('EMAIL_ADDRESS')
email_password = os.getenv('EMAIL_PASSWORD')
smtp_server = os.getenv('SMTP_SERVER')
smtp_port = os.getenv('SMTP_PORT')
tracking_base_url = os.getenv('TRACKING_BASE_URL')

print("Environment Variables Test:")
print(f"Email Address: {email_address}")
print(f"Email Password: {'*' * len(email_password) if email_password else 'None'}")
print(f"SMTP Server: {smtp_server}")
print(f"SMTP Port: {smtp_port}")
print(f"Tracking Base URL: {tracking_base_url}")

# Check if all required variables are loaded
required_vars = ['EMAIL_ADDRESS', 'EMAIL_PASSWORD', 'SMTP_SERVER', 'SMTP_PORT', 'TRACKING_BASE_URL']
missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    print(f"\n❌ Missing environment variables: {missing_vars}")
else:
    print("\n✅ All environment variables loaded successfully!")
