import os
import glob

import psycopg
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}


def main():
    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("CREATE SCHEMA IF NOT EXISTS healthcare;")
            cur.execute("SET search_path TO healthcare;")

            # Create tables
            for migration in sorted(glob.glob("migrations/*.sql")):
                print(f"Running {migration}")
                with open(migration, "r", encoding="utf-8") as f:
                    cur.execute(f.read())

            load_order = [
                "patients",
                "doctors",
                "appointments",
                "prescriptions",
                "lab_results"
            ]

            for table in load_order:
                csv_file = f"data/{table}.csv"

                print(f"Loading {csv_file} -> {table}")

                with open(csv_file, "rb") as f:
                    with cur.copy(
                        f"COPY healthcare.{table} FROM STDIN WITH CSV HEADER"
                    ) as copy:
                        while chunk := f.read(8192):
                            copy.write(chunk)

            # Load CSV data
            # for csv_file in sorted(glob.glob("data/*.csv")):
            #     table = os.path.splitext(os.path.basename(csv_file))[0]

            #     print(f"Loading {csv_file} -> {table}")

            #     with open(csv_file, "rb") as f:
            #         with cur.copy(
            #             f"COPY healthcare.{table} FROM STDIN WITH CSV HEADER"
            #         ) as copy:
            #             while chunk := f.read(8192):
            #                 copy.write(chunk)

        conn.commit()

    print("\nAll data loaded successfully.")


if __name__ == "__main__":
    main()