

CREATE TABLE lab_results (
    result_id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL,
    test_name VARCHAR(255) NOT NULL,
    test_date DATE NOT NULL,
    result_value FLOAT NOT NULL,
    unit VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);
