from datetime import datetime, timedelta

from modules.gmail_reader import get_gmail_service, search_emails
from database.database import get_connection
from services.email_sender import send_email


def free_pratique_exists(vessel):

    service = get_gmail_service()

    query = f'"{vessel}" AND (Free Pratique OR "Livre prática" OR CLP)'

    results = search_emails(service, query)

    return len(results) > 0


def check_free_pratique():

    conn = get_connection()
    cursor = conn.cursor()

    rows = cursor.execute("""
        SELECT vessels.id, vessels.name, vessels.branch, prospects.eta
        FROM vessels
        JOIN prospects
        ON vessels.id = prospects.vessel_id
    """).fetchall()

    for row in rows:

        vessel = row["name"]
        eta = row["eta"]

        if not eta:
            continue

        try:
            eta_date = datetime.strptime(eta, "%d/%m")
        except:
            continue

        if eta_date - datetime.today() <= timedelta(days=5):

            if not free_pratique_exists(vessel):

                cursor.execute("""
                    INSERT INTO alerts (vessel_id, branch, alert_type, created_at)
                    VALUES (?, ?, ?, ?)
                """, (
                    row["id"],
                    row["branch"],
                    "Free pratique pending",
                    datetime.now()
                ))

                send_email(
                    f"Reminder: Free Pratique not issued for {vessel}",
                    f"Free pratique has not been detected for vessel {vessel}.",
                    "operations@company.com"
                )

    conn.commit()
    conn.close()