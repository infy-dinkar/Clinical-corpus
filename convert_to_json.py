import json

input_file = "500_ner_snippets.txt"
output_file = "500_ner_snippets.json"

data = []

with open(input_file, "r", encoding="utf-8") as f:
    content = f.read().strip()

snippets = content.split("\n\n")

for snip in snippets:
    data.append({"text": snip})

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("JSON file created")