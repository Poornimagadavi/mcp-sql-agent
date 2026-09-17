
CREATE TABLE patients (
    patient_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    gender VARCHAR(10),
    blood_group VARCHAR(10),
    city VARCHAR(100),
    phone BIGINT,
    email VARCHAR(100)
);



