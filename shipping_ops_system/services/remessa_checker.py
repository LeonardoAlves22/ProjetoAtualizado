from datetime import datetime

from modules.gmail_reader import get_gmail_service, search_emails
from database.database import get_connection


def remessa_exists(vessel):

    service = get_gmail_service()

    query = f'"{vessel}" AND "CADASTRO DE REMESSA"'

    results = search_emails(service, query)

    return len(results) > 0


def check_remessa():

    conn = get_connection()
    cursor = conn.cursor()

    vessels = cursor.execute("""
        SELECT id, name, branch
        FROM vessels
    """).fetchall()

    for row in vessels:

        vessel = row["name"]

        if not remessa_exists(vessel):

            cursor.execute("""
                INSERT INTO alerts (vessel_id, branch, alert_type, created_at)
                VALUES (?, ?, ?, ?)
            """, (
                row["id"],
                row["branch"],
                "Remessa missing",
                datetime.now()
            ))

    conn.commit()
    conn.close()