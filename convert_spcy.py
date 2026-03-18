import json

# 👇 yaha apna export file daal
INPUT_FILE = "project-4-at-2026-03-18-13-28-f12dc46a.json"
OUTPUT_FILE = "spacy_clean_final.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

spacy_data = []
error_count = 0
fixed_count = 0

for task in data:
    text = task["data"]["text"]

    if not task.get("annotations"):
        continue

    entities = []

    for ann in task["annotations"][0]["result"]:
        value = ann["value"]

        start = value["start"]
        end = value["end"]
        label = value["labels"][0]

        # 🔥 FIX 1: remove leading space
        while start < end and text[start] == " ":
            start += 1

        # 🔥 FIX 2: remove trailing space
        while end > start and text[end - 1] == " ":
            end -= 1

        # 🔥 FIX 3: skip invalid
        if start >= end:
            error_count += 1
            continue

        entity_text = text[start:end]

        # 🔥 FIX 4: strip safety
        stripped = entity_text.strip()

        if entity_text != stripped:
            diff_left = len(entity_text) - len(entity_text.lstrip())
            diff_right = len(entity_text) - len(entity_text.rstrip())

            start += diff_left
            end -= diff_right
            fixed_count += 1

        # 🔥 FIX 5: final check
        if start >= end:
            error_count += 1
            continue

        entities.append((start, end, label))

    # skip agar entity hi nahi hai
    if len(entities) == 0:
        continue

    spacy_data.append((text, {"entities": entities}))

# save
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(spacy_data, f, indent=2)

print("✅ Conversion + Cleaning Done")
print(f"Total samples: {len(spacy_data)}")
print(f"Fixed spans: {fixed_count}")
print(f"Removed invalid spans: {error_count}")