import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASS = os.getenv("GMAIL_APP_PASSWORD")


def send_email(subject, body, recipient):

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = GMAIL_USER
    msg["To"] = recipient

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)

    server.login(GMAIL_USER, GMAIL_PASS)

    server.sendmail(GMAIL_USER, [recipient], msg.as_string())

    server.quit()