from Bio import Entrez
import nltk
import random
from datetime import datetime, timedelta

nltk.download("punkt")

Entrez.email = "dinkarthakur120@gmail.com"

TARGET = 200

# Patient names
patient_names = [
"Rahul Verma","Ramesh Kumar","Sunita Sharma","Anita Mishra",
"Vikas Singh","Priya Gupta","Sanjay Tiwari","Arjun Mehta",
"Neha Singh","Kavita Sharma","Soumya Chatterjee","Arindam Ghosh",
"Anupam Banerjee","Debasis Roy","Pradeep Pattnaik",
"Debasis Mohanty","Sanjay Behera","Madhusmita Das",
"Subramaniam Venkataraman","Lakshmi Narayanan",
"S. Krishnan","R. Raghavan"
]

doctors = [
"R.K. Mehta","Anjali Rao","S. Krishnan","Debasis Roy","Arindam Ghosh"
]

hospitals = [
"AIIMS New Delhi",
"Apollo Hospital Chennai",
"Fortis Hospital Kolkata",
"KIMS Hospital Bhubaneswar",
"Narayana Health Bengaluru"
]

def random_age():
    return f"{random.randint(18,80)}-year-old"

def random_phone():
    return str(random.randint(9000000000,9999999999))

def random_abha():
    return f"{random.randint(10,99)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}"

def random_date():
    start = datetime(2021,1,1)
    end = datetime(2025,12,31)
    delta = end - start
    d = start + timedelta(days=random.randint(0, delta.days))
    return d.strftime("%d %B %Y")

def relation():
    if random.random() < 0.5:
        return "s/o " + random.choice(patient_names)
    else:
        return "w/o " + random.choice(patient_names)

print("Searching PubMed...")

search = Entrez.esearch(
    db="pubmed",
    term="case report patient hospital",
    retmax=500
)

ids = Entrez.read(search)["IdList"]

snippets = []

for pmid in ids:

    fetch = Entrez.efetch(
        db="pubmed",
        id=pmid,
        rettype="abstract",
        retmode="text"
    )

    text = fetch.read()

    sentences = nltk.sent_tokenize(text)

    for s in sentences:

        if "patient" in s.lower() or "year-old" in s.lower():

            name = random.choice(patient_names)
            rel = relation()

            snippet = f"""{name} {rel}, a {random_age()} patient, presented to {random.choice(hospitals)} on {random_date()} with complaints noted in the clinical report. The patient was evaluated by Dr. {random.choice(doctors)}. Hospital records include contact number {random_phone()} and ABHA ID {random_abha()}. {s}"""

            snippets.append(snippet)

            if len(snippets) >= TARGET:
                break

    if len(snippets) >= TARGET:
        break

with open("pub_ner_snippets_200.txt","w",encoding="utf8") as f:
    for s in snippets:
        f.write(s + "\n\n")

print("200 NER snippets generated → ner_snippets_200.txt")