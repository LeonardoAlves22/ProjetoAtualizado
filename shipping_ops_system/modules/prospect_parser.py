import re
from datetime import datetime


ALLOWED_SENDERS = [
    "operation.sluis@wilsonsons.com.br",
    "operation.belem@wilsonsons.com.br",
    "agencybrazil@cargill.com",
    "wsliner.belem@wilsonsons.com.br"
]


def valid_prospect_subject(subject):

    keywords = [
        "prospect",
        "prospects",
        "daily notice",
        "berthing",
        "line up",
        "line-up"
    ]

    subject = subject.lower()

    return any(word in subject for word in keywords)
    
def body_contains_schedule(body):

    if not body:
        return False

    text = body.lower()

    keywords = ["eta", "etb", "etd"]

    return any(word in text for word in keywords)

def classify_prospect_time(email_date):

    hour = email_date.hour
    minute = email_date.minute

    if hour < 13 or (hour == 13 and minute <= 30):
        return "morning"

    return "afternoon"


def normalize(text):

    text = text.upper()

    text = text.replace("-", " ")
    text = text.replace("/", " ")
    text = text.replace("\n", " ")

    text = re.sub(r"\s+", " ", text)

    # remover prefixos comuns
    text = re.sub(r"\bM\s?V\.?\s+", "", text)

    return text.strip()


def detect_vessels(subject, body, vessel_list):

    detected = []

    text = normalize(subject + " " + body)

    for vessel in vessel_list:

        vessel_name = normalize(vessel)

        if re.search(rf"\b{re.escape(vessel_name)}\b", text):
            detected.append(vessel)

    return list(set(detected))


def extract_vessel_list(email_body):

    vessel_list = {
        "SLZ": [],
        "BELEM": []
    }

    # remover assinatura
    text = email_body.split("Best Regards")[0]

    current_branch = None

    lines = text.splitlines()

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if line.upper() == "SLZ":
            current_branch = "SLZ"
            continue

        if line.upper() == "BELEM":
            current_branch = "BELEM"
            continue

        if current_branch:

            # evitar linhas que não são navios
            if len(line) < 3:
                continue

            if "@" in line:
                continue

            vessel_list[current_branch].append(line.upper())

    return vessel_list
from datetime import datetime


ALLOWED_SENDERS = [
    "operation.sluis@wilsonsons.com.br",
    "operation.belem@wilsonsons.com.br",
    "agencybrazil@cargill.com",
    "wsliner.belem@wilsonsons.com.br"
]


def valid_prospect_subject(subject):

    keywords = [
        "prospect",
        "prospects",
        "daily notice",
        "berthing",
        "line up",
        "line-up"
    ]

    subject = subject.lower()

    return any(word in subject for word in keywords)


def classify_prospect_time(email_date):

    hour = email_date.hour
    minute = email_date.minute

    if hour < 13 or (hour == 13 and minute <= 30):
        return "morning"

    return "afternoon"


def normalize(text):

    text = text.upper()

    text = text.replace("-", " ")
    text = text.replace("/", " ")
    text = text.replace("\n", " ")

    text = re.sub(r"\s+", " ", text)

    # remover prefixos comuns
    text = re.sub(r"\bM\s?V\.?\s+", "", text)

    return text.strip()


def normalize_text(text):

    text = text.upper()

    # substituir caracteres especiais
    text = text.replace("-", " ")
    text = text.replace("/", " ")

    # remover múltiplos espaços
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def detect_vessels(subject, body, vessel_list):

    detected = []

    body_clean = normalize_text(body)

    for vessel in vessel_list:

        vessel_clean = normalize_text(vessel)

        if vessel_clean in body_clean:

            detected.append(vessel)

    return detected


def extract_vessel_list(email_body):

    vessel_list = {
        "SLZ": [],
        "BELEM": []
    }

    # remover assinatura
    text = email_body.split("Best Regards")[0]

    current_branch = None

    lines = text.splitlines()

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if line.upper() == "SLZ":
            current_branch = "SLZ"
            continue

        if line.upper() == "BELEM":
            current_branch = "BELEM"
            continue

        if current_branch:

            # evitar linhas que não são navios
            if len(line) < 3:
                continue

            if "@" in line:
                continue

            vessel_list[current_branch].append(line.upper())

    return vessel_list