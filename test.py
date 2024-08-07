import ssl
import imaplib

imap_url = 'imap.gmail.com'
context = ssl.create_default_context()
try:
    imap = imaplib.IMAP4_SSL(imap_url, ssl_context=context)
    print("Connection successful")
except Exception as e:
    print(f"Error: {e}")

