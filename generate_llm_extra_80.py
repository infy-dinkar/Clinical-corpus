import json
import random

output_file = "llm_generated_extra_80.json"

first_names = [
    "Ravi", "Amit", "Sanjay", "Rahul", "Priya", "Neha", "Anita", "Kavita", "Sunita", "Pooja",
    "Venkataraman", "Krishnamurthy", "Suresh", "Ramesh", "Lakshmi", "Meena", "Anirban", "Subhasish"
]

last_names = [
    "Sharma", "Verma", "Singh", "Gupta", "Mishra", "Das", "Pattnaik", "Ghosh", "Raghavan",
    "Nair", "Pillai", "Chatterjee", "Bandyopadhyay", "Mukherjee", "Patnaik", "Mohapatra", "Behera"
]

hospitals = [
    "AIIMS New Delhi",
    "Apollo Hospital Chennai",
    "Fortis Hospital Kolkata",
    "KIMS Hospital Bhubaneswar",
    "Narayana Health Bengaluru"
]

doctors = [
    "Dr. R.K. Mehta",
    "Dr. Anjali Rao",
    "Dr. Debasis Roy",
    "Dr. Arindam Ghosh",
    "Dr. S. Krishnan"
]

def random_phone():
    return str(random.randint(9000000000, 9999999999))

def random_abha():
    return f"{random.randint(10,99)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}"

def random_date():
    days = random.randint(1,28)
    months = [
        "January","February","March","April","May","June",
        "July","August","September","October","November","December"
    ]
    return f"{days} {random.choice(months)} {random.randint(2021,2025)}"

generated = []

for _ in range(80):

    # 🔥 FULL NAME FIX (main part)
    relation = random.choice(['s/o','w/o'])

    patient_name = f"{random.choice(first_names)} {random.choice(last_names)}"
    guardian_name = f"{random.choice(first_names)} {random.choice(last_names)}"

    name = f"{patient_name} {relation} {guardian_name}"

    age = f"{random.randint(18,85)}-year-old"
    hospital = random.choice(hospitals)
    date = random_date()
    doctor = random.choice(doctors)
    phone = random_phone()
    abha = random_abha()

    sentence = f"{name}, a {age} patient, presented to {hospital} on {date} with complaints recorded in the clinical report. The patient was evaluated by {doctor}. Hospital records include contact number {phone} and ABHA ID {abha}. The patient reported symptoms such as fatigue, dizziness, and mild fever. Clinical examination and investigations were performed, and appropriate treatment was initiated."

    generated.append({
        "data": {
            "text": sentence
        }
    })

# save file
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(generated, f, indent=4, ensure_ascii=False)

print("✅ Generated 80 realistic synthetic entries")