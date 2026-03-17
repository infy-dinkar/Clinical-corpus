import json

# -------- FILE LIST --------
files = [
    "pub_ner_clean_200.json",
    "pmc_ner_clean_150.json",
    "llm_ner_context_fixed.json",
    "llm_generated_extra_80.json"
]

final_data = []

# -------- LOAD & MERGE --------
for file in files:
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            final_data.extend(data)
            print(f"Loaded {file} → {len(data)} entries")
    except Exception as e:
        print(f"Error loading {file}: {e}")

# -------- FINAL COUNT --------
total = len(final_data)
print(f"\n Total merged entries: {total}")

# -------- SAVE --------
output_file = "500_ner_records.json"

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(final_data, f, indent=4, ensure_ascii=False)

print(f"Saved as {output_file}")