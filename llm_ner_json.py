import re
import json

input_file = "llm_clinical_ner_snippets_150.txt"
output_file = "llm_ner_context_fixed.json"

with open(input_file, "r", encoding="utf-8") as f:
    text = f.read()

# -------- REMOVE TAGS --------
text = re.sub(r"<[^>]+>", " ", text)
text = re.sub(r"&[a-z]+;", " ", text)

# -------- CLEAN --------
text = re.sub(r"\s+", " ", text).strip()

# -------- SPLIT --------
records = re.split(r"\n\s*\n|\*\*", text)

cleaned = []

for rec in records:
    rec = rec.strip()

    if len(rec) < 80:
        continue

    # -------- RELAXED CHECK --------
    has_name = re.search(r"\b(?:s/o|w/o)\b", rec)
    has_age = re.search(r"\b\d{1,3}", rec)
    has_abha = re.search(r"\d{2}-\d{4}-\d{4}-\d{4}", rec)

    # minimum 3 important entities
    if sum([bool(has_name), bool(has_age), bool(has_abha)]) >= 2:

        rec = re.sub(r"\s+", " ", rec).strip()

        cleaned.append({
            "data": {
                "text": rec
            }
        })

# -------- COUNT --------
total = len(cleaned)
print(f"\n✅ Total entries: {total}")

# -------- SAVE --------
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(cleaned, f, indent=4, ensure_ascii=False)

print(f"✅ Saved as {output_file}")