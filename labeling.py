import json
import re

input_file = "500_ner_records.json"
output_file = "auto_labeled.json"

def find_entities(text):

    entities = []

    # 🔥 1. PATIENT + RELATIVE NAME

    relation_pattern = r'^([A-Z][a-zA-Z\.]+(?: [A-Z][a-zA-Z]+)+)\s+(s/o|w/o|d/o|h/o)\s+([A-Z][a-zA-Z\.]+(?: [A-Z][a-zA-Z]+)+)'
    match = re.search(relation_pattern, text)

    if match:
        entities.append((match.start(1), match.end(1), "PATIENT_NAME"))
        entities.append((match.start(3), match.end(3), "RELATIVE_NAME"))

    else:
        match = re.match(r'^([A-Z][a-zA-Z\.]+(?: [A-Z][a-zA-Z]+)+)', text)
        if match:
            entities.append((match.start(1), match.end(1), "PATIENT_NAME"))

    # 🔥 2. DOCTOR (with initials)
    for match in re.finditer(r'Dr\. ([A-Z][a-zA-Z\.]+(?: [A-Z][a-zA-Z]+)+)', text):
        entities.append((match.start(1), match.end(1), "DOCTOR"))

    # 🔥 3. PHONE
    for match in re.finditer(r'\b[6-9]\d{9}\b', text):
        entities.append((match.start(), match.end(), "PHONE_NUMBER"))

    # 🔥 4. ABHA
    for match in re.finditer(r'\b\d{2}-\d{4}-\d{4}-\d{4}\b', text):
        entities.append((match.start(), match.end(), "ABHA_ID"))

    # 🔥 5. DATE
    for match in re.finditer(
        r'\b\d{1,2} (January|February|March|April|May|June|July|August|September|October|November|December) \d{4}\b',
        text):
        entities.append((match.start(), match.end(), "DATE"))

    # 🔥 6. AGE (ONLY FIRST)
    match = re.search(r'\b\d{1,3}-year-old\b', text)
    if match:
        entities.append((match.start(), match.end(), "AGE"))

    # 🔥 7. HOSPITAL NAME (UPGRADED LOGIC)

    hospital_found = False

    # ✅ METHOD 1: context-based
    context_pattern = r'presented to ([A-Z][A-Za-z ]+?) on'
    match = re.search(context_pattern, text)

    if match:
        hospital = match.group(1)

        # validate hospital-like keywords
        if any(word in hospital for word in ["Hospital", "Health", "Clinic", "Centre", "Institute", "AIIMS"]):
            entities.append((match.start(1), match.end(1), "HOSPITAL_NAME"))
            hospital_found = True

    # ✅ METHOD 2: strong direct match (AIIMS + known hospitals)
    if not hospital_found:
        strong_pattern = r'\b(AIIMS [A-Za-z ]+|Apollo Hospital [A-Za-z ]+|Fortis Hospital [A-Za-z ]+|KIMS Hospital [A-Za-z ]+|Narayana Health [A-Za-z ]+)\b'

        for match in re.finditer(strong_pattern, text):
            entities.append((match.start(), match.end(), "HOSPITAL_NAME"))
            hospital_found = True

    # ✅ METHOD 3: generic fallback
    if not hospital_found:
        generic_pattern = r'\b([A-Z][a-zA-Z]+(?: [A-Z][a-zA-Z]+)* (Hospital|Clinic|Centre|Institute|Medical College|Healthcare|Health))\b'

        for match in re.finditer(generic_pattern, text):
            entities.append((match.start(), match.end(), "HOSPITAL_NAME"))

    # 🔥 REMOVE DUPLICATES
    entities = sorted(set(entities), key=lambda x: x[0])

    return entities


# LOAD DATA
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

output = []

for item in data:

    text = item["data"]["text"]
    entities = find_entities(text)

    result = []

    for start, end, label in entities:
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
        "data": {
            "text": text
        },
        "predictions": [
            {
                "result": result
            }
        ]
    })

# SAVE
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=4, ensure_ascii=False)

print("✅ FINAL script with AIIMS + all hospitals fixed 🚀")