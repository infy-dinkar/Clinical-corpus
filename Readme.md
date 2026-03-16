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

* `s/o` and `w/o` relationships
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


