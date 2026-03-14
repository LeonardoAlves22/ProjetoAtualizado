from datetime import datetime, timedelta

from modules.gmail_reader import get_gmail_service, search_emails
from database.database import get_connection


def entry_clearance_exists(vessel):

    service = get_gmail_service()

    query = f'"{vessel}" AND ("Anuência de Entrada" OR "Entry clearance")'

    results = search_emails(service, query)

    return len(results) > 0


def departure_clearance_exists(vessel):

    service = get_gmail_service()

    query = f'"{vessel}" AND ("Anuência de Saída" OR "Departure clearance")'

    results = search_emails(service, query)

    return len(results) > 0


def check_entry_clearance():

    conn = get_connection()
    cursor = conn.cursor()

    rows = cursor.execute("""
        SELECT vessels.id, vessels.name, vessels.branch, prospects.etb
        FROM vessels
        JOIN prospects
        ON vessels.id = prospects.vessel_id
    """).fetchall()

    for row in rows:

        vessel = row["name"]
        etb = row["etb"]

        if not etb:
            continue

        try:
            etb_date = datetime.strptime(etb, "%d/%m")
        except:
            continue

        if etb_date - datetime.today() <= timedelta(days=1):

            if not entry_clearance_exists(vessel):

                cursor.execute("""
                    INSERT INTO alerts (vessel_id, branch, alert_type, created_at)
                    VALUES (?, ?, ?, ?)
                """, (
                    row["id"],
                    row["branch"],
                    "Entry clearance missing",
                    datetime.now()
                ))

    conn.commit()
    conn.close()


def check_departure_clearance():

    conn = get_connection()
    cursor = conn.cursor()

    rows = cursor.execute("""
        SELECT vessels.id, vessels.name, vessels.branch, prospects.etd
        FROM vessels
        JOIN prospects
        ON vessels.id = prospects.vessel_id
    """).fetchall()

    for row in rows:

        vessel = row["name"]
        etd = row["etd"]

        if not etd:
            continue

        try:
            etd_date = datetime.strptime(etd, "%d/%m")
        except:
            continue

        if etd_date - datetime.today() <= timedelta(days=1):

            if not departure_clearance_exists(vessel):

                cursor.execute("""
                    INSERT INTO alerts (vessel_id, branch, alert_type, created_at)
                    VALUES (?, ?, ?, ?)
                """, (
                    row["id"],
                    row["branch"],
                    "Departure clearance missing",
                    datetime.now()
                ))

    conn.commit()
    conn.close()