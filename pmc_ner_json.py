import json
import re

input_file = "pmc_ner_snippets_150.txt"
output_file = "pmc_ner_clean_150.json"

with open(input_file, "r", encoding="utf-8") as f:
    text = f.read()

# 1. XML / tag cleanup
text = re.sub(r"<[^>]+>", " ", text)

# 2. Extra spaces/newlines cleanup
text = re.sub(r"\s+", " ", text).strip()

# 3. Split by patient pattern
# Example: Arjun Mehta w/o Sunita Sharma ...
pattern = r"(?=(?:[A-Z][a-zA-Z.]*\s){1,3}(?:w/o|s/o)\s(?:[A-Z][a-zA-Z.]*\s?){1,3},\s*a\s+\d{1,3}-year-old\s+patient)"

snippets = re.split(pattern, text)

cleaned = []

for snip in snippets:
    snip = snip.strip()

    if len(snip) < 50:
        continue

    # Remove common junk fragments
    snip = re.sub(r"\b(?:xref|ref-type|rid|colspan|rowspan|tbody|thead|table-wrap|table|label|caption)\b.*?(?=\.|,|;)", " ", snip, flags=re.IGNORECASE)
    snip = re.sub(r"\s+", " ", snip).strip()

    # Keep only snippets that look like proper target records
    has_name_relation = re.search(r"\b(?:w/o|s/o)\b", snip)
    has_age = re.search(r"\b\d{1,3}-year-old\b", snip)
    has_hospital = re.search(r"\b(?:AIIMS New Delhi|Apollo Hospital Chennai|Fortis Hospital Kolkata|KIMS Hospital Bhubaneswar|Narayana Health Bengaluru)\b", snip)
    has_date = re.search(r"\b\d{1,2}\s+[A-Z][a-z]+\s+\d{4}\b", snip)
    has_doctor = re.search(r"\bDr\.\s*[A-Z][a-zA-Z. ]+", snip)
    has_phone = re.search(r"\b\d{10}\b", snip)
    has_abha = re.search(r"\b\d{2}-\d{4}-\d{4}-\d{4}\b", snip)

    if all([has_name_relation, has_age, has_hospital, has_date, has_doctor, has_phone, has_abha]):
        cleaned.append({
            "data": {
                "text": snip
            }
        })

total = len(cleaned)
print(f"\n✅ Total PMC entries after cleaning: {total}")

if total == 150:
    print("🎯 PERFECT: Exactly 150 entries")
else:
    print("⚠️ Not exactly 150 — check output once")

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(cleaned, f, indent=4, ensure_ascii=False)

print(f"✅ Saved as {output_file}")