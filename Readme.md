```markdown
# Indian Clinical NER Corpus – Data Generation

This repository contains scripts used to generate a synthetic and semi-synthetic corpus for **Indian clinical Named Entity Recognition (NER)** experiments.
The goal of the dataset is to produce clinical text snippets that resemble common documentation used in hospitals while ensuring that **no real patient data is included**.

The dataset is created by combining three sources of text:

1. PubMed abstracts
2. PubMed Central (PMC) clinical case reports
3. LLM-generated synthetic clinical notes

Each snippet is constructed so that common clinical entities appear in realistic contexts.

---

## Entity Types Included

Every snippet is designed to contain the following entity types:

* Patient Name (including Indian naming patterns)
* ABHA ID
* Doctor Name
* Hospital Name
* Phone Number
* Date (Indian formats)
* Age expressions

Examples of patterns used include:

* `s/o`, `w/o`, `d/o`, `h/o` relationships
* hyphenated ABHA IDs (e.g. `12-3456-7890-1234`)
* age expressions such as `45-year-old`
* Indian hospital names and doctor designations

---

## Data Generation Sources

### 1. PubMed Abstract Extraction

Clinical sentences are retrieved from the **PubMed database** using the official Entrez API provided by the National Center for Biotechnology Information (NCBI).

The script:

* searches PubMed for clinical case related abstracts
* downloads abstracts programmatically
* extracts sentences containing clinical context
* injects structured entities such as ABHA ID, phone numbers, and hospital names where necessary

Script used:

```

generate_ner_snippets.py

```

Output:

```

pub_ner_snippets_200.txt

```

Total snippets generated from PubMed: **200**

---

### 2. PubMed Central (PMC) Case Reports

Full clinical case descriptions are retrieved from **PubMed Central (PMC)**.

The script:

* searches PMC for case report articles
* extracts sentences referencing patients or clinical findings
* injects structured identifiers and demographic details to ensure entity coverage

Script used:

```

generate_pmc_snippets.py

```

Output:

```

pmc_ner_snippets_150.txt

```

Total snippets generated from PMC: **150**

---

### 3. LLM-Generated Synthetic Clinical Notes

To increase linguistic variety and simulate realistic hospital documentation, additional clinical notes are generated using a **Large Language Model (LLM)**.

The model generates multiple types of clinical documentation including:

* Discharge Notes
* SOAP Notes
* Prescription Notes
* IPD Round Notes

Each prompt includes predefined entities such as:

* patient name
* hospital name
* doctor name
* ABHA ID
* phone number
* date
* age pattern

The LLM rewrites these prompts into natural clinical documentation style text while preserving the entities.

Script used:

```

generate_llm_clinical_notes.py

```

Output:

```

llm_clinical_ner_snippets_150.txt

```

Total synthetic snippets generated: **150**

---

## Dataset Composition

| Source                       | Number of Snippets |
| ---------------------------- | ------------------ |
| PubMed                       | 200                |
| PubMed Central (PMC)         | 150                |
| LLM Synthetic Clinical Notes | 150                |

Total snippets generated:

```

500 clinical text snippets

```

---

## Privacy and Data Safety

The dataset intentionally **does not contain real patient records**.

* Public biomedical literature (PubMed / PMC) is used only for clinical language patterns.
* Identifiable information such as ABHA IDs, phone numbers, and patient names are synthetically generated.
* No protected health information (PHI) from real medical records is included.

---

## Generated Output Files

```

pub_ner_snippets_200.txt
pmc_ner_snippets_150.txt
llm_clinical_ner_snippets_150.txt

```

---

# NEW UPDATES (DATA PIPELINE + ANNOTATION)

## 🔧 Data Processing Added

After initial generation, the dataset is further processed to make it **model-ready**:

* Cleaning of noisy text (removal of tags, formatting issues)
* Preservation of clinical context
* Conversion to structured JSON format
* Validation of entity presence

Generated JSON files:

```

pub_ner_clean_200.json
pmc_ner_clean_150.json
llm_ner_context_fixed.json

```

---

## Synthetic Data Augmentation

To improve dataset diversity and balance:

Script used:

```

generate_llm_extra_80.py

```

Output:

```

llm_generated_extra_80.json

```

---

## Final Dataset Merge

All datasets are merged into a single file:

Script:

```

merge_all_json.py

```

Final Output:

```

500_ner_records.json

```

Final dataset size:

```

~500+ clinical NER samples

```

---

## 🏷️ Label Studio Annotation Setup

The dataset is annotated using **Label Studio**.

### Installation

```

pip install label-studio

```

### Run

```

label-studio

```

Open in browser:

```

[http://localhost:8080](http://localhost:8080)

```

---

# AUTO LABELING + FINAL DATASET

## 🔗 Auto Labeling Pipeline

The dataset is automatically labeled using:

```

adv_labelling.py

```

### Features:

* Detects all entity types
* Supports Indian relationship connectors:
  `s/o`, `w/o`, `d/o`, `h/o`
* Ensures each record contains all required entities
* Automatically rebuilds incomplete samples

---

## Final Labeled Dataset

```

500_ner_records.json       → raw merged dataset
adv_auto_labeled.json     → backup / intermediate output
adv_auto_labeled1.json    → final auto-labeled dataset (USED FOR TRAINING)
auto_labeled.json         → earlier version of auto-labeling (kept for reference and comparison)

````

---

##  Label Studio Config (UPDATED)

```xml
<View>
  <Labels name="label" toName="text">

    <Label value="PATIENT_NAME"/>
    <Label value="RELATIVE_NAME"/>
    <Label value="AGE"/>
    <Label value="HOSPITAL_NAME"/>
    <Label value="DATE"/>
    <Label value="DOCTOR"/>
    <Label value="PHONE_NUMBER"/>
    <Label value="ABHA_ID"/>

  </Labels>

  <Text name="text" value="$text"/>
</View>
````

**Note:** Label names are aligned with the final JSON (`adv_auto_labeled1.json`).

---

## 🔧 Data Cleaning Update

During final validation, a small number of samples (2 records) were found where the `PATIENT_NAME` and `RELATIVE_NAME` were identical.

These records were logically inconsistent and could negatively impact model learning.

Hence, they were removed from the dataset to maintain data quality and correctness.

removing_duplicated.py is removing the duplicates and producing a proper cleaned file as final_clean_adv_auto_labeled1.json.

Final dataset size after cleaning: **514 samples**

## Important Notes

* `adv_auto_labeled.json` has **NOT been deleted intentionally**
  → kept for:

  * future understanding
  * debugging
  * making improvements

* `convert_spcy.py` has **NOT been executed yet**
  → If required, simply run:

```
python convert_spcy.py
```

→ It will generate spaCy-compatible training data.

---

## Final Outcome

The dataset ensures:

* All required entity types are present
* Indian naming diversity is preserved
* All relationship connectors are covered
* No real patient data (PII) is used

---






