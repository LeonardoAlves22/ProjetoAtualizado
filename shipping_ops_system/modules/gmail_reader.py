import base64
from email import message_from_bytes
from email.utils import parsedate_to_datetime

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import pytz
import time
import base64
from email import message_from_bytes
from bs4 import BeautifulSoup

from bs4 import BeautifulSoup

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


# ---------------------------------------------------
# CONECTAR AO GMAIL
# ---------------------------------------------------

def get_gmail_service():

    creds = Credentials.from_authorized_user_file(
        "token.json",
        SCOPES
    )

    service = build("gmail", "v1", credentials=creds)

    return service


# ---------------------------------------------------
# BUSCAR EMAILS
# ---------------------------------------------------

def search_emails(service, query):

    result = service.users().messages().list(
        userId="me",
        q=query,
        maxResults=30
    ).execute()

    messages = result.get("messages", [])

    return messages
def get_email_subject(service, msg_id):

    msg = service.users().messages().get(
        userId="me",
        id=msg_id,
        format="metadata",
        metadataHeaders=["Subject"]
    ).execute()

    headers = msg["payload"]["headers"]

    for h in headers:
        if h["name"] == "Subject":
            return h["value"]

    return ""

# ---------------------------------------------------
# OBTER CORPO DO EMAIL
# ---------------------------------------------------

def get_email_body(service, msg_id):

    attempts = 3

    for attempt in range(attempts):

        try:

            msg = service.users().messages().get(
                userId="me",
                id=msg_id,
                format="raw"
            ).execute()

            raw = base64.urlsafe_b64decode(msg["raw"].encode("ASCII"))

            mime_msg = message_from_bytes(raw)

            body = ""

            if mime_msg.is_multipart():

                for part in mime_msg.walk():

                    content_type = part.get_content_type()

                    if content_type == "text/plain":

                        payload = part.get_payload(decode=True)

                        if payload:
                            body += payload.decode(errors="ignore")

                    elif content_type == "text/html":

                        payload = part.get_payload(decode=True)

                        if payload:

                            html = payload.decode(errors="ignore")

                            soup = BeautifulSoup(html, "html.parser")

                            body += soup.get_text()

            else:

                payload = mime_msg.get_payload(decode=True)

                if payload:
                    body = payload.decode(errors="ignore")

            return body

        except Exception as e:

            print(f"Erro ao ler email {msg_id}: {e}")

            time.sleep(2)

    return ""

# ---------------------------------------------------
# OBTER DATA DO EMAIL
# ---------------------------------------------------

def get_email_metadata(service, msg_id):

    msg = service.users().messages().get(
        userId="me",
        id=msg_id,
        format="metadata",
        metadataHeaders=["Date"]
    ).execute()

    headers = msg["payload"]["headers"]

    for h in headers:

        if h["name"] == "Date":

            email_date = parsedate_to_datetime(h["value"])

            # converter para horário Brasil
            brasil = pytz.timezone("America/Sao_Paulo")

            return email_date.astimezone(brasil)

    return None