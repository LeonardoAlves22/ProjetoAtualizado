import re
from datetime import datetime

MONTHS = {
    "JAN": "01","FEB": "02","MAR": "03","APR": "04",
    "MAY": "05","JUN": "06","JUL": "07","AUG": "08",
    "SEP": "09","OCT": "10","NOV": "11","DEC": "12"
}

def normalize_date(date_str):

    date_str = date_str.strip().upper()

    # formato 15/06/2026
    if re.match(r"\d{1,2}/\d{1,2}/\d{4}", date_str):
        d = datetime.strptime(date_str,"%d/%m/%Y")
        return d.strftime("%d-%m-%Y")

    # formato 15/06
    if re.match(r"\d{1,2}/\d{1,2}", date_str):
        d = datetime.strptime(date_str,"%d/%m")
        return d.strftime("%d-%m")

    # formato 15 JUN
    parts = date_str.split()

    if len(parts) == 2:

        day = parts[0]
        month = MONTHS.get(parts[1])

        if month:
            return f"{day}-{month}"

    return None


def extract_dates(text):

    patterns = {
        "ETA": r"ETA[^0-9A-Z]{0,5}([0-9]{1,2}[/\-][0-9]{1,2}([/\-][0-9]{2,4})?|[0-9]{1,2}\s[A-Z]{3})",
        "ETB": r"ETB[^0-9A-Z]{0,5}([0-9]{1,2}[/\-][0-9]{1,2}([/\-][0-9]{2,4})?|[0-9]{1,2}\s[A-Z]{3})",
        "ETD": r"ETD[^0-9A-Z]{0,5}([0-9]{1,2}[/\-][0-9]{1,2}([/\-][0-9]{2,4})?|[0-9]{1,2}\s[A-Z]{3})",
    }

    results = {}

    text = text.upper()

    for key,pattern in patterns.items():

        match = re.search(pattern,text)

        if match:

            raw = match.group(1)

            results[key] = normalize_date(raw)

        else:

            results[key] = None

    return results