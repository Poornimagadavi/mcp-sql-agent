
CREATE TABLE prescriptions (
    prescription_id BIGSERIAL PRIMARY KEY,
    patient_id BIGINT REFERENCES patients(patient_id),
    doctor_id BIGINT REFERENCES doctors(doctor_id),
    medicine VARCHAR(255),
    dosage VARCHAR(255),
    duration_days INT,
    prescription_date DATE
);

