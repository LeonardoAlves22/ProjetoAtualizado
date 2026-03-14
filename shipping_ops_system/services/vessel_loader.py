from modules.gmail_reader import search_emails

from modules.prospect_parser import extract_vessel_list
from database.database import get_connection


def load_vessels():

    service = get_gmail_service()

    messages = search_emails(service, 'subject:"LISTA NAVIOS"')

    print("Emails encontrados:", messages)

    if not messages:
        print("Nenhum email LISTA NAVIOS encontrado")
        return

    msg_id = messages[0]["id"]

    body = get_email_body(service, msg_id)

    print("BODY DO EMAIL:")
    print(body)

    vessel_list = extract_vessel_list(body)

    print("VESSELS EXTRAIDOS:", vessel_list)

    conn = get_connection()
    cursor = conn.cursor()

    for branch in vessel_list:

        for vessel in vessel_list[branch]:

            cursor.execute("""
            INSERT OR IGNORE INTO vessels (name,branch)
            VALUES (?,?)
            """, (vessel,branch))

    conn.commit()
    conn.close()

    return vessel_list
