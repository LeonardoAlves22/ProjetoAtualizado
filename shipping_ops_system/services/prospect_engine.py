from modules.gmail_reader import search_emails
from modules.prospect_parser import (
    detect_vessels,
    valid_prospect_subject,
    body_contains_schedule
)


def process_prospects(vessel_list):

    # buscar emails com prospect
    emails = search_emails("prospect")

    results = []

    if not emails:
        return results

    for mail in emails:

        subject = mail["subject"]
        body = mail["body"]

        if not subject:
            continue

        # verificar se é prospect notice
        if not valid_prospect_subject(subject):
            continue

        # verificar se tem ETA / ETB / ETD no corpo
        if not body_contains_schedule(body):
            continue

        # detectar navios
        vessels_found = detect_vessels(subject, body, vessel_list)

        if not vessels_found:
            continue

        for vessel in vessels_found:

            results.append({
                "vessel": vessel,
                "subject": subject,
                "status": "prospect_detected"
            })

    return results
