
CREATE TABLE doctors (
    doctor_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    specialization VARCHAR(255),
    hospital VARCHAR(255),
    city VARCHAR(255),
    experience_years INT
);

