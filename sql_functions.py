
import os
import json
import sqlite3
# import base64
import datetime

from gmail_functions import (
 
    get_messages
)



# SQLite database configuration
DB_FILE = 'emails.db'
# Store emails in the database
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Create SQLite database table for emails
def create_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS emails (
                        id TEXT PRIMARY KEY,
                        from_email TEXT,
                        subject TEXT,
                        message TEXT,
                        received_date DATETIME,
                        is_read INTEGER,
                        is_processed INTEGER,
                        folder TEXT default 'INBOX'
                    )''')
    conn.commit()
    conn.close()

# Fetch emails from Gmail API and store them in the database
def fetch_emails():
    
    
    
    email_list = get_messages()
    for email_data in email_list:
        cursor.execute('''INSERT OR REPLACE INTO emails
                            (id, from_email, subject, message, received_date, is_read, is_processed)
                            VALUES (?, ?, ?, ?, ?, ?, ?)''',
                        (email_data['id'], email_data['from_email'], email_data['subject'],
                        email_data['message'], email_data['received_date'], email_data['is_read'],
                        email_data['is_processed']))
    conn.commit()
    # conn.close()

def execute_query(query):
    print(query)
    q=cursor.execute(query)
    conn.commit()
    return [row[0] for row in cursor.fetchall()]
    # conn.close()