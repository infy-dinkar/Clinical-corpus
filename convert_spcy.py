import json
import random
import spacy
from spacy.tokens import DocBin
from spacy.training import Example

# Load your exported Label Studio JSON
with open("adv_auto_labeled1.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Convert Label Studio format to spaCy (text, {"entities": [(start, end, label)]})
def convert(ls_data):
    training = []
    for item in ls_data:
        text = item["data"]["text"]
        entities = []

        # Check both "annotations" and "predictions" (auto-labeled data uses "predictions")
        sources = item.get("annotations", []) + item.get("predictions", [])

        for ann in sources:
            for result in ann.get("result", []):
                if result["type"] == "labels":
                    start = result["value"]["start"]
                    end = result["value"]["end"]
                    label = result["value"]["labels"][0]
                    entities.append((start, end, label))

        training.append((text, {"entities": entities}))
    return training

all_data = convert(data)

# Stratified 80/20 split — shuffle then split
random.seed(42)
random.shuffle(all_data)
split = int(len(all_data) * 0.8)
train_data = all_data[:split]
dev_data = all_data[split:]

# Save to .spacy files
nlp = spacy.blank("en")

def save_spacy(data, path):
    db = DocBin()
    for text, annotations in data:
        doc = nlp.make_doc(text)
        ents = []
        for start, end, label in annotations["entities"]:
            span = doc.char_span(start, end, label=label)
            if span is not None:
                ents.append(span)
        doc.ents = ents
        db.add(doc)
    db.to_disk(path)

save_spacy(train_data, "train.spacy")
save_spacy(dev_data, "dev.spacy")
print(f"train: {len(train_data)}, dev: {len(dev_data)}")