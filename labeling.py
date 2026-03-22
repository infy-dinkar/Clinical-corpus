import json
import re

input_file = "500_ner_records.json"
output_file = "auto_labeled.json"

def find_entities(text):

    entities = []

    # 1. PATIENT NAME (start of sentence)
    match = re.match(r'^([A-Z][a-z]+ [A-Z][a-z]+)', text)
    if match:
        entities.append((match.start(), match.end(), "PATIENT_NAME"))

    # 2. DOCTOR (WITHOUT "Dr.")
    for match in re.finditer(r'Dr\. ([A-Z][a-z]+ [A-Z][a-z]+)', text):
        start = match.start(1)
        end = match.end(1)
        entities.append((start, end, "DOCTOR"))

    # 3. PHONE NUMBER
    for match in re.finditer(r'\b[6-9]\d{9}\b', text):
        entities.append((match.start(), match.end(), "PHONE_NUMBER"))

    # 4. ABHA ID
    for match in re.finditer(r'\b\d{2}-\d{4}-\d{4}-\d{4}\b', text):
        entities.append((match.start(), match.end(), "ABHA_ID"))

    # 5. DATE
    for match in re.finditer(
        r'\b\d{1,2} (January|February|March|April|May|June|July|August|September|October|November|December) \d{4}\b',
        text):
        entities.append((match.start(), match.end(), "DATE"))

    # 6. AGE (ONLY NUMBER)
    for match in re.finditer(r'\b(\d{1,3})-year-old\b', text):
        start = match.start(1)
        end = match.end(1)
        entities.append((start, end, "AGE"))

    # 🔥 7. HOSPITAL NAME (HYBRID FIXED)

    hospital_found = False

    # METHOD 1: Context-based (priority)
    for match in re.finditer(r'presented to (.*?) on', text):
        entities.append((match.start(1), match.end(1), "HOSPITAL_NAME"))
        hospital_found = True

    # METHOD 2: Keyword fallback (only if context not found)
    if not hospital_found:
        hospital_keywords = [
            "Hospital", "Clinic", "Centre", "Center",
            "Medical College", "Institute", "Nursing Home",
            "Healthcare", "Health", "Care"
        ]

        pattern = r'\b([A-Z][a-zA-Z]+(?: [A-Z][a-zA-Z]+)* (' + '|'.join(hospital_keywords) + r'))\b'

        for match in re.finditer(pattern, text):
            entities.append((match.start(), match.end(), "HOSPITAL_NAME"))

    # 🔥 REMOVE DUPLICATES + SORT
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

# SAVE FILE
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=4, ensure_ascii=False)

print("✅ Final clean auto-labeled dataset ready 🚀")