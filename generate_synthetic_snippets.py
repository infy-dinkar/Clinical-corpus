import os
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
from groq import Groq
from tqdm import tqdm

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

TARGET = 150

patient_names = [
"Rahul Verma","Ramesh Kumar","Sunita Sharma","Anita Mishra",
"Vikas Singh","Priya Gupta","Sanjay Tiwari","Arjun Mehta",
"Neha Singh","Kavita Sharma","Soumya Chatterjee","Arindam Ghosh",
"Anupam Banerjee","Debasis Roy","Pradeep Pattnaik",
"Debasis Mohanty","Sanjay Behera","Madhusmita Das",
"Subramaniam Venkataraman","Lakshmi Narayanan"
]

doctors = [
"R.K. Mehta","Anjali Rao","S. Krishnan",
"Debasis Roy","Arindam Ghosh"
]

hospitals = [
"AIIMS New Delhi",
"Apollo Hospital Chennai",
"Fortis Hospital Kolkata",
"KIMS Hospital Bhubaneswar",
"Narayana Health Bengaluru"
]

symptoms = [
"persistent cough","abdominal pain","fever and chills",
"shortness of breath","severe headache","dizziness",
"chest pain","fatigue","nausea and vomiting"
]

note_types = [
"Discharge Note",
"SOAP Note",
"Prescription Note",
"IPD Round Note"
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

def build_prompt():

    name = random.choice(patient_names)
    rel = relation()
    age = random_age()
    doctor = random.choice(doctors)
    hospital = random.choice(hospitals)
    symptom = random.choice(symptoms)
    date = random_date()
    phone = random_phone()
    abha = random_abha()
    note_type = random.choice(note_types)

    prompt = f"""
Write a realistic {note_type} from an Indian hospital.

Include the following entities exactly as written:

Patient: {name} {rel}
Age: {age}
Hospital: {hospital}
Doctor: Dr. {doctor}
Date: {date}
Phone: {phone}
ABHA ID: {abha}
Symptom: {symptom}

Use natural hospital documentation language.
Do not modify the entities above.
"""

    return prompt


def generate_note(prompt):

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role":"user","content":prompt}],
        temperature=0.8
    )

    return response.choices[0].message.content.strip()


notes = []

for _ in tqdm(range(TARGET)):

    prompt = build_prompt()

    note = generate_note(prompt)

    notes.append(note)


with open("llm_clinical_ner_snippets_150.txt","w",encoding="utf8") as f:

    for n in notes:
        f.write(n + "\n\n")


print("150 clinical notes generated → llm_clinical_ner_snippets_150.txt") 