from modules.gmail_reader import (
    get_gmail_service,
    search_emails,
    get_email_body,
    get_email_metadata
)

from modules.prospect_parser import detect_vessels, valid_prospect_subject, body_contains_schedule
from modules.eta_extractor import extract_dates
from modules.gmail_reader import get_email_subject

from database.database import get_connection

from datetime import datetime
import pytz


def process_prospects(vessel_list):

    service = get_gmail_service()

    # buscar apenas prospects recentes
    messages = search_emails(service, "label:PROSPECT newer_than:1d")

    conn = get_connection()
    cursor = conn.cursor()

    brasil = pytz.timezone("America/Sao_Paulo")

    now = datetime.now(brasil)
    today = now.date()

    # limpar prospects antigos
    cursor.execute("""
        DELETE FROM prospects
        WHERE date < ?
    """, (today,))

    for msg in messages:

        msg_id = msg["id"]

        email_date = get_email_metadata(service, msg_id)

        if not email_date:
            continue

        # ignorar emails de dias anteriores
        if email_date.date() != today:
            continue

        body = get_email_body(service, msg_id)

        if not body:
            continue

        print("\n----------------------------")
        print("EMAIL ID:", msg_id)
        print("EMAIL BODY:")
        print(body)
        print("----------------------------")

        subject = get_email_subject(service, msg_id)
        body = get_email_body(service, msg_id)

# verificar se é prospect
        if not valid_prospect_subject(subject):
            continue

    # verificar se corpo tem ETA / ETB / ETD
        if not body_contains_schedule(body):
            continue
        vessels = detect_vessels(subject, body, vessel_list)

        print("VESSELS DETECTED:", vessels)

        if not vessels:
            continue

        classification = classify_prospect_time(email_date)

        for vessel in vessels:

            cursor.execute(
                "SELECT id FROM vessels WHERE name=?",
                (vessel,)
            )

            row = cursor.fetchone()

            if not row:
                continue

            vessel_id = row["id"]

            lines = body.splitlines()

            eta = None
            etb = None
            etd = None

            for i, line in enumerate(lines):

                if vessel.upper() in line.upper():

                    dates = extract_dates(line)

                    eta = dates["ETA"]
                    etb = dates["ETB"]
                    etd = dates["ETD"]

                    # procurar datas nas próximas linhas
                    for j in range(i + 1, min(i + 4, len(lines))):

                        nearby = extract_dates(lines[j])

                        if not eta and nearby["ETA"]:
                            eta = nearby["ETA"]

                        if not etb and nearby["ETB"]:
                            etb = nearby["ETB"]

                        if not etd and nearby["ETD"]:
                            etd = nearby["ETD"]

                    break

            prospect_morning = 1 if classification == "morning" else 0
            prospect_afternoon = 1 if classification == "afternoon" else 0

            print("SAVING PROSPECT:", vessel)

            cursor.execute("""
                INSERT INTO prospects
                (vessel_id, date, prospect_morning, prospect_afternoon, eta, etb, etd, email_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                vessel_id,
                email_date.date(),
                prospect_morning,
                prospect_afternoon,
                eta,
                etb,
                etd,
                msg_id
            ))

    conn.commit()
    conn.close()