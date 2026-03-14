import imaplib
import email
import streamlit as st


def get_gmail_connection():

    user = st.secrets["GMAIL_USER"]
    password = st.secrets["GMAIL_APP_PASSWORD"]

    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(user, password)

    return mail


def search_emails(subject_filter):

    mail = get_gmail_connection()

    mail.select("inbox")

    status, messages = mail.search(None, f'(SUBJECT "{subject_filter}")')

    email_ids = messages[0].split()

    emails = []

    for e_id in email_ids[-20:]:

        status, msg_data = mail.fetch(e_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])

        subject = msg["subject"]

        body = ""

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode(errors="ignore")
        else:
            body = msg.get_payload(decode=True).decode(errors="ignore")

        emails.append({
            "subject": subject,
            "body": body
        })

    return emails