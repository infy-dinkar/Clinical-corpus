import json

INPUT_FILE = "adv_auto_labeled1.json"
OUTPUT_FILE = "spacy_clean_final.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

spacy_data = []
error_count = 0
fixed_count = 0

print(f"Total tasks loaded: {len(data)}")

for task in data:

    text = task["data"]["text"]

    # 🔥 use predictions
    if not task.get("predictions") or len(task["predictions"]) == 0:
        # keep empty sample also (important)
        spacy_data.append((text, {"entities": []}))
        continue

    entities = []

    for ann in task["predictions"][0]["result"]:

        value = ann["value"]

        start = value["start"]
        end = value["end"]
        label = value["labels"][0]

        # 🔥 fix leading spaces
        while start < end and text[start] == " ":
            start += 1

        # 🔥 fix trailing spaces
        while end > start and text[end - 1] == " ":
            end -= 1

        if start >= end:
            error_count += 1
            continue

        entity_text = text[start:end]

        # 🔥 strip fix
        stripped = entity_text.strip()

        if entity_text != stripped:
            diff_left = len(entity_text) - len(entity_text.lstrip())
            diff_right = len(entity_text) - len(entity_text.rstrip())

            start += diff_left
            end -= diff_right
            fixed_count += 1

        if start >= end:
            error_count += 1
            continue

        entities.append((start, end, label))

    # 🔥 remove duplicates
    entities = list(set(entities))

    # 🔥 remove overlaps (keep longest)
    clean_entities = []
    last_end = -1

    for start, end, label in sorted(entities, key=lambda x: (x[0], -(x[1]-x[0]))):
        if start >= last_end:
            clean_entities.append((start, end, label))
            last_end = end

    entities = clean_entities

    # 🔥 KEEP ONLY FIRST OCCURRENCE PER LABEL
    filtered_entities = []
    seen_labels = set()

    for start, end, label in entities:
        if label not in seen_labels:
            filtered_entities.append((start, end, label))
            seen_labels.add(label)

    entities = filtered_entities

    # 🔥 IMPORTANT: DO NOT DROP SAMPLE
    spacy_data.append((text, {"entities": entities}))

# SAVE
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(spacy_data, f, indent=2, ensure_ascii=False)

print("✅ Conversion + Cleaning Done")
print(f"Total samples: {len(spacy_data)}")
print(f"Fixed spans: {fixed_count}")
print(f"Removed invalid spans: {error_count}")