import json
import re

input_file = "adv_auto_labeled1.json"
output_file = "final_clean_adv_auto_labeled1.json"

def extract_names(text):
    match = re.search(r'([A-Z][a-zA-Z]+ [A-Z][a-zA-Z]+)\s+(s/o|w/o|d/o|h/o)\s+([A-Z][a-zA-Z]+ [A-Z][a-zA-Z]+)', text)
    if match:
        return match.group(1).strip(), match.group(3).strip()
    return None, None


with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

clean_data = []
removed_count = 0

for item in data:
    text = item["data"]["text"]
    patient, relative = extract_names(text)

    if patient and relative and patient == relative:
        removed_count += 1
        continue  # ❌ skip bad record

    clean_data.append(item)

print("Removed records:", removed_count)
print("Final count:", len(clean_data))

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(clean_data, f, indent=2, ensure_ascii=False)

print("✅ Clean dataset saved as final_clean.json")