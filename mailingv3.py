import base64
import os.path
import pickle
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# OAuth 2.0 scopes needed for Gmail
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Email configuration
sender_email = "placement@iiitt.ac.in"
batch_size = 100
pause_interval = 200
skip_first_row = False

# Email content
subject = "Invitation to conduct Training and Placement Drive at IIIT Tiruchirappalli"

def get_gmail_service():
    """Authenticate and create a Gmail service object."""
    creds = None
    
    # The file token.pickle stores the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Manual OAuth flow process
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            
            # Generate authorization URL
            auth_url, _ = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true'
            )
            
            print('Please go to this URL and authorize access:')
            print(auth_url)
            
            # Wait for authorization and get the code
            code = input('Enter the authorization code: ')
            
            # Exchange code for tokens
            flow.fetch_token(code=code)
            creds = flow.credentials
        
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    # Return Gmail API service
    return build('gmail', 'v1', credentials=creds)

def create_message(sender, to, subject, message_text):
    """Create a message for an email."""
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    
    message.attach(MIMEText(message_text, 'html'))
    
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    return {'raw': raw_message}

def send_message(service, user_id, message):
    """Send an email message."""
    try:
        message = service.users().messages().send(
            userId=user_id, body=message).execute()
        print(f"Message Id: {message['id']}")
        return message
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

def send_emails(recipients, email_body):
    """Send emails to a list of recipients."""
    # Get authenticated Gmail service
    service = get_gmail_service()
    
    # Keep track of emails sent for batching
    emails_sent = 0
    
    for i, recipient in enumerate(recipients):
        if skip_first_row and i == 0:
            continue
            
        # Create and send email
        message = create_message(sender_email, recipient, subject, email_body)
        send_message(service, 'me', message)
        
        print(f"Email sent to {recipient}")
        emails_sent += 1
        
        # Pause after sending a batch of emails
        if emails_sent % batch_size == 0:
            print(f"Pausing for {pause_interval} seconds after sending {batch_size} emails...")
            time.sleep(pause_interval)
            
    print(f"Total emails sent: {emails_sent}")

def main():
    # Example usage
    # Load your recipients list from a file or database
    recipients = ["211105@iiitt.ac.in"]  # Replace with your actual recipients
    
    # Your email body (HTML format)
    email_body = """
    <html>
    <body>
        <p>Dear Sir/Madam,</p>
        <p>Your email content here...</p>
    </body>
    </html>
    """
    
    send_emails(recipients, email_body)

if __name__ == "__main__":
    main()