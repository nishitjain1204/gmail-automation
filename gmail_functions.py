
import base64
# from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import googleapiclient

from datetime import datetime
from dateutil import parser

# Gmail API credentials
CLIENT_SECRET_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']



# Authenticate to Gmail API
def authenticate():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    creds = flow.run_local_server(port=8000)
    return creds

creds = authenticate()
service = build('gmail', 'v1', credentials=creds)

# Get the value of a specific header field from email
def get_header_value(email):
    
    headers = email.get('payload', {}).get('headers', [])
    op_header = dict()
    
    for header in headers:
        
        if header['name'] in ('From','Subject','Date'):
            op_header[header['name']] = header['value']
            
    return op_header

# Get the body of the email message
def get_message_body(email):
    parts = email.get('payload', {}).get('parts', [])
    for part in parts:
        if part['mimeType'] == 'text/plain':
            data = part.get('body', {}).get('data')
            if data:
                return base64.urlsafe_b64decode(data).decode()
    return ''

# Mark email as read in Gmail
def mark_email_as_read(email_id):
    
    mark = service.users().messages().modify(userId='me', id=email_id, body={'removeLabelIds': ['UNREAD']}).execute()
    # print(mark)

# Mark email as unread in Gmail
def mark_email_as_unread(email_id):
    try:
        
        mark= service.users().messages().modify(userId='me', id=email_id, body={'addLabelIds': ['UNREAD']}).execute()
        return True if mark else False
    except googleapiclient.errors.HttpError:
        return False

def get_messages():
    
   
    date_format = "%a, %d %b %Y %H:%M:%S"
    
    # Fetch list of emails from Inbox
    folder = 'INBOX'
    results = service.users().messages().list(userId='me' , labelIds=[folder] ).execute()
    messages = results.get('messages', [])
    email_list = []
    
    for message in messages:
        
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        
        header_value = get_header_value(msg)
        
        date_string = header_value.get('Date')
        
        datetime_obj = parser.parse(date_string)
        email_data = {
            'id': msg['id'],
            'from_email': header_value.get('From'),
            'subject': header_value.get('Subject'),
            'message': get_message_body(msg),
            'received_date': datetime_obj.strftime("%Y-%m-%d %H:%M:%S"),
            'is_read': int('UNREAD' not in msg['labelIds']),
            'is_processed': 0,
            'folder':folder
        }
        email_list.append(email_data)
        
    return email_list

# Move an email to a folder (label)
def move_email_to_folder(message_id=None, folder_name=None):
    try:
       
        labels = service.users().labels().list(userId='me').execute().get('labels',[])
      
        for label in labels:
            
            if label['name'] == folder_name:
                label_id = label['id']
        
        modify_request = {
            'addLabelIds': [label_id]
            }     
           
        service.users().messages().modify(userId='me', id=message_id,body=modify_request).execute()
    except googleapiclient.errors.HttpError:
        
        return False
    

def get_valid_folders():
    labels = service.users().labels().list(userId='me').execute().get('labels', [])
    return [label['name'] for label in labels]
    
    