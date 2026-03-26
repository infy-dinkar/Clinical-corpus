import json
import re
import random

input_file = "500_ner_records.json"
output_file = "adv_auto_labeled1.json"

# 🔥 INDIAN DIVERSITY

first_names = ["Arjun","Ravi","Neha","Priya","Lakshmi","Venkatesh","Rahul","Anita","Soumya","Debasis"]
last_names = ["Sharma","Verma","Singh","Iyer","Nair","Pillai","Chatterjee","Mukherjee","Patnaik","Mohapatra"]

hospitals = [
    "AIIMS New Delhi","Apollo Hospital Chennai","Fortis Hospital Kolkata",
    "KIMS Hospital Bhubaneswar","Narayana Health Bengaluru","PGIMER Chandigarh",
    "CMC Vellore","NIMHANS Bengaluru","Tata Memorial Hospital Mumbai"
]

doctors = ["Anjali Rao","R.K. Mehta","S. Krishnan","Debasis Roy","Arindam Ghosh"]

months = ["January","February","March","April","May","June","July","August","September","October","November","December"]

# 🔥 CONNECTORS (FIXED)
connectors = ["s/o", "w/o", "d/o", "h/o"]

def rand_name():
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def rand_phone():
    return str(random.randint(9000000000,9999999999))

def rand_abha():
    return f"{random.randint(10,99)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}"

def rand_date():
    return f"{random.randint(1,28)} {random.choice(months)} {random.randint(2021,2025)}"

def rand_age():
    return f"{random.randint(18,85)}-year-old"


def rebuild(text):
    """Rebuild sentence from scratch → safest way"""

    patient = rand_name()
    relative = rand_name()
    hospital = random.choice(hospitals)
    doctor = random.choice(doctors)
    phone = rand_phone()
    abha = rand_abha()
    date = rand_date()
    age = rand_age()

    # 🔥 RANDOM CONNECTOR (FIX)
    connector = random.choice(connectors)

    new_text = (
        f"{patient} {connector} {relative}, a {age} patient, presented to {hospital} on {date}. "
        f"Evaluated by Dr. {doctor}. Contact number {phone}. ABHA ID {abha}."
    )

    return new_text


def find_entities(text):

    entities = []

    # 🔥 PATIENT + RELATIVE (FIXED REGEX)
    match = re.search(
        r'([A-Z][a-zA-Z]+ [A-Z][a-zA-Z]+)\s+(s/o|w/o|d/o|h/o)\s+([A-Z][a-zA-Z]+ [A-Z][a-zA-Z]+)',
        text
    )
    if match:
        entities.append((match.start(1), match.end(1), "PATIENT_NAME"))
        entities.append((match.start(3), match.end(3), "RELATIVE_NAME"))

    # AGE
    match = re.search(r'\b\d{1,3}-year-old\b', text)
    if match:
        entities.append((match.start(), match.end(), "AGE"))

    # HOSPITAL
    match = re.search(r'presented to ([A-Z][A-Za-z ]+?) on', text)
    if match:
        entities.append((match.start(1), match.end(1), "HOSPITAL_NAME"))

    # DATE
    for m in re.finditer(r'\b\d{1,2} [A-Za-z]+ \d{4}\b', text):
        entities.append((m.start(), m.end(), "DATE"))

    # DOCTOR
    for m in re.finditer(r'Dr\. ([A-Z][a-zA-Z\.]+(?: [A-Z][a-zA-Z]+)+)', text):
        entities.append((m.start(1), m.end(1), "DOCTOR"))

    # PHONE
    for m in re.finditer(r'\b[6-9]\d{9}\b', text):
        entities.append((m.start(), m.end(), "PHONE_NUMBER"))

    # ABHA
    for m in re.finditer(r'\b\d{2}-\d{4}-\d{4}-\d{4}\b', text):
        entities.append((m.start(), m.end(), "ABHA_ID"))

    return sorted(set(entities), key=lambda x: x[0])


# 🔥 MAIN

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

output = []

for item in data:

    text = item["data"]["text"]

    entities = find_entities(text)
    labels_present = set([e[2] for e in entities])

    required = ["PATIENT_NAME","RELATIVE_NAME","AGE","HOSPITAL_NAME","DATE","DOCTOR","PHONE_NUMBER","ABHA_ID"]

    # 🔥 IF ANY MISSING → FULL REBUILD
    if not all(r in labels_present for r in required):
        text = rebuild(text)
        entities = find_entities(text)

    result = []

    for start,end,label in entities:
        result.append({
            "value": {
                "start": start,
                "end": end,
                "text": text[start:end],
                "labels": [label]
            },
            "from_name": "label",
            "to_name": "text",
            "type": "labels"
        })

    output.append({
        "data": {"text": text},
        "predictions": [{"result": result}]
    })

# SAVE
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=4, ensure_ascii=False)

print("✅ FINAL FIXED: All connectors (s/o, w/o, d/o, h/o) included 🚀")