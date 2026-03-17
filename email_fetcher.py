import imaplib
import email
from email.header import decode_header

def fetch_emails(username, password, limit=10):
    mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    mail.login(username, password)
    mail.select("Inbox")
    status, messages = mail.search(None, "ALL")
    email_ids = messages[0].split()
    emails = []

    for e_id in email_ids[-limit:]:
        status, msg_data = mail.fetch(e_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(msg["subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode()
                body = ""

                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        if content_type =="text/plain":
                            body = part.get_payload(decode=True).decode(errors="ignore")
                            break
                else:
                    body = msg.get_payload(decode=True).decode(errors="ignore")
                emails.append({
                    "subject": subject,
                    "body": body
                })
    mail.logout()
    return emails