import os
import random
from datetime import datetime, timedelta

import pandas as pd


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

random.seed(42)

OUTPUT_DIR = "data"

NUM_PATIENTS = 2000
NUM_DOCTORS = 100
NUM_APPOINTMENTS = 8000
NUM_PRESCRIPTIONS = 6000
NUM_LAB_RESULTS = 10000


# ---------------------------------------------------------
# Helper data
# ---------------------------------------------------------

FIRST_NAMES = [
    "Aarav", "Aditi", "Arjun", "Ananya", "Rahul",
    "Priya", "Rohan", "Sneha", "Vikram", "Neha",
    "Karan", "Pooja", "Amit", "Kavya", "Nikhil",
    "Meera", "Raj", "Isha", "Varun", "Riya",
    "Sanjay", "Simran", "Aditya", "Shreya", "Manish",
    "Divya", "Akash", "Nisha", "Vivek", "Swati"
]

LAST_NAMES = [
    "Sharma", "Patel", "Gupta", "Mehta", "Verma",
    "Reddy", "Iyer", "Nair", "Singh", "Joshi",
    "Desai", "Kulkarni", "Kapoor", "Malhotra", "Rao",
    "Chopra", "Mishra", "Bansal", "Khan", "Das"
]

CITIES = [
    "Mumbai",
    "Pune",
    "Delhi",
    "Bangalore",
    "Hyderabad",
    "Chennai",
    "Kolkata",
    "Ahmedabad",
    "Jaipur",
    "Lucknow"
]

GENDERS = ["Male", "Female"]

BLOOD_GROUPS = [
    "A+", "A-", "B+", "B-",
    "AB+", "AB-", "O+", "O-"
]

SPECIALIZATIONS = [
    "Cardiology",
    "Neurology",
    "Orthopedics",
    "Dermatology",
    "Pediatrics",
    "General Medicine",
    "Gynecology",
    "Oncology",
    "ENT",
    "Gastroenterology"
]

HOSPITALS = [
    "CityCare Hospital",
    "Apollo Medical Center",
    "Fortis Healthcare",
    "Global Health Hospital",
    "Sunrise Hospital",
    "Metro Medical Center",
    "LifeLine Hospital",
    "GreenView Hospital"
]

APPOINTMENT_STATUSES = [
    "Completed",
    "Scheduled",
    "Cancelled",
    "No Show"
]

APPOINTMENT_REASONS = [
    "Routine Checkup",
    "Follow-up",
    "Chest Pain",
    "Fever",
    "Headache",
    "Back Pain",
    "Skin Problem",
    "Joint Pain",
    "Stomach Pain",
    "Diabetes Consultation",
    "Blood Pressure Check"
]

MEDICINES = [
    "Paracetamol",
    "Amoxicillin",
    "Azithromycin",
    "Ibuprofen",
    "Metformin",
    "Atorvastatin",
    "Omeprazole",
    "Cetirizine",
    "Pantoprazole",
    "Amlodipine",
    "Losartan",
    "Vitamin D3",
    "Calcium",
    "Levothyroxine",
    "Montelukast"
]

DOSAGES = [
    "250 mg",
    "500 mg",
    "10 mg",
    "20 mg",
    "40 mg",
    "5 mg",
    "100 mg"
]

LAB_TESTS = {
    "Hemoglobin": ("g/dL", 8.0, 18.0),
    "Glucose": ("mg/dL", 60.0, 250.0),
    "Cholesterol": ("mg/dL", 100.0, 300.0),
    "Blood Pressure": ("mmHg", 80.0, 180.0),
    "Vitamin D": ("ng/mL", 5.0, 80.0),
    "Creatinine": ("mg/dL", 0.4, 3.0),
    "TSH": ("mIU/L", 0.1, 12.0),
    "Platelet Count": ("10^3/uL", 100.0, 500.0)
}


# ---------------------------------------------------------
# Utility functions
# ---------------------------------------------------------

def random_date(start_date, end_date):
    """Generate a random date between two dates."""
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)


def random_name():
    return (
        random.choice(FIRST_NAMES),
        random.choice(LAST_NAMES)
    )


# ---------------------------------------------------------
# Generate Patients
# ---------------------------------------------------------

def generate_patients():
    patients = []

    for patient_id in range(1, NUM_PATIENTS + 1):
        first_name, last_name = random_name()
        name = f"{first_name} {last_name}"

        age = random.randint(1, 85)
        gender = random.choice(GENDERS)
        blood_group = random.choice(BLOOD_GROUPS)
        city = random.choice(CITIES)

        phone = f"9{random.randint(100000000, 999999999)}"

        email_name = (
            f"{first_name.lower()}."
            f"{last_name.lower()}"
            f"{patient_id}"
        )

        email = f"{email_name}@example.com"

        patients.append({
            "patient_id": patient_id,
            "name": name,
            "age": age,
            "gender": gender,
            "blood_group": blood_group,
            "city": city,
            "phone": phone,
            "email": email
        })

    return pd.DataFrame(patients)


# ---------------------------------------------------------
# Generate Doctors
# ---------------------------------------------------------

def generate_doctors():
    doctors = []

    for doctor_id in range(1, NUM_DOCTORS + 1):
        first_name, last_name = random_name()

        doctors.append({
            "doctor_id": doctor_id,
            "name": f"Dr. {first_name} {last_name}",
            "specialization": random.choice(SPECIALIZATIONS),
            "hospital": random.choice(HOSPITALS),
            "city": random.choice(CITIES),
            "experience_years": random.randint(2, 35)
        })

    return pd.DataFrame(doctors)


# ---------------------------------------------------------
# Generate Appointments
# ---------------------------------------------------------

def generate_appointments():
    appointments = []

    start_date = datetime(2024, 1, 1)
    end_date = datetime(2026, 9, 1)

    for appointment_id in range(1, NUM_APPOINTMENTS + 1):
        patient_id = random.randint(1, NUM_PATIENTS)
        doctor_id = random.randint(1, NUM_DOCTORS)

        appointment_date = random_date(
            start_date,
            end_date
        ).date()

        appointments.append({
            "appointment_id": appointment_id,
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_date": appointment_date,
            "status": random.choice(APPOINTMENT_STATUSES),
            "reason": random.choice(APPOINTMENT_REASONS)
        })

    return pd.DataFrame(appointments)


# ---------------------------------------------------------
# Generate Prescriptions
# ---------------------------------------------------------

def generate_prescriptions():
    prescriptions = []

    start_date = datetime(2024, 1, 1)
    end_date = datetime(2026, 9, 1)

    for prescription_id in range(1, NUM_PRESCRIPTIONS + 1):
        patient_id = random.randint(1, NUM_PATIENTS)
        doctor_id = random.randint(1, NUM_DOCTORS)

        prescription_date = random_date(
            start_date,
            end_date
        ).date()

        prescriptions.append({
            "prescription_id": prescription_id,
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "medicine": random.choice(MEDICINES),
            "dosage": random.choice(DOSAGES),
            "duration_days": random.randint(3, 90),
            "prescription_date": prescription_date
        })

    return pd.DataFrame(prescriptions)


# ---------------------------------------------------------
# Generate Lab Results
# ---------------------------------------------------------

def generate_lab_results():
    lab_results = []

    start_date = datetime(2024, 1, 1)
    end_date = datetime(2026, 9, 1)

    for result_id in range(1, NUM_LAB_RESULTS + 1):
        patient_id = random.randint(1, NUM_PATIENTS)

        test_name = random.choice(
            list(LAB_TESTS.keys())
        )

        unit, min_value, max_value = LAB_TESTS[test_name]

        result_value = round(
            random.uniform(min_value, max_value),
            2
        )

        # Some values are intentionally abnormal
        # so we can test analytical SQL queries later.
        if random.random() < 0.15:
            result_value = round(
                max_value * random.uniform(1.05, 1.30),
                2
            )

        test_date = random_date(
            start_date,
            end_date
        ).date()

        status = random.choice([
            "Normal",
            "Normal",
            "Normal",
            "Abnormal"
        ])

        lab_results.append({
            "result_id": result_id,
            "patient_id": patient_id,
            "test_name": test_name,
            "test_date": test_date,
            "result_value": result_value,
            "unit": unit,
            "status": status
        })

    return pd.DataFrame(lab_results)


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("Generating synthetic healthcare data...\n")

    patients = generate_patients()
    doctors = generate_doctors()
    appointments = generate_appointments()
    prescriptions = generate_prescriptions()
    lab_results = generate_lab_results()

    datasets = {
        "patients.csv": patients,
        "doctors.csv": doctors,
        "appointments.csv": appointments,
        "prescriptions.csv": prescriptions,
        "lab_results.csv": lab_results
    }

    for filename, dataframe in datasets.items():

        path = os.path.join(
            OUTPUT_DIR,
            filename
        )

        dataframe.to_csv(
            path,
            index=False
        )

        print(
            f"✓ {filename:<20} "
            f"{len(dataframe):>6} rows"
        )

    print("\nData generation completed.")
    print(f"Files saved in: {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()