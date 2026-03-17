import json
import re

input_file = "pub_ner_snippets_200.txt"
output_file = "pub_ner_clean_200.json"

with open(input_file, "r", encoding="utf-8") as f:
    text = f.read()

# STEP 1: split entries
snippets = text.split("\n\n")

cleaned = []

for snip in snippets:
    snip = snip.strip()

    if len(snip) < 30:
        continue

    # remove XML / tags
    snip = re.sub(r'<.*?>', '', snip)

    # remove unwanted keywords
    snip = re.sub(r'\b(xref|table|figure|et al)\b', '', snip, flags=re.IGNORECASE)

    # clean spaces
    snip = re.sub(r'\s+', ' ', snip)

    cleaned.append({
        "data": {
            "text": snip.strip()
        }
    })

#  COUNT CHECK
total = len(cleaned)
print(f"\n✅ Total entries after cleaning: {total}")

# OPTIONAL VALIDATION
if total == 200:
    print("PERFECT: Exactly 200 entries")
else:
    print("WARNING: Not exactly 200 — check splitting")

# SAVE JSON
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(cleaned, f, indent=4)

print(f"✅ Saved as {output_file}")