import json
import os

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
    os.makedirs("metadata", exist_ok=True)

    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:

            cur.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'healthcare'
                AND table_type = 'BASE TABLE'
                ORDER BY table_name;
            """)
            tables = [row[0] for row in cur.fetchall()]

            metadata = {
                "schema": "healthcare",
                "tables": {}
            }

            for table in tables:

                cur.execute("""
                    SELECT
                        column_name,
                        data_type,
                        is_nullable
                    FROM information_schema.columns
                    WHERE table_schema = 'healthcare'
                    AND table_name = %s
                    ORDER BY ordinal_position;
                """, (table,))

                columns = [
                    {
                        "name": row[0],
                        "type": row[1],
                        "nullable": row[2] == "YES"
                    }
                    for row in cur.fetchall()
                ]

                cur.execute("""
                    SELECT kcu.column_name
                    FROM information_schema.table_constraints tc
                    JOIN information_schema.key_column_usage kcu
                      ON tc.constraint_name = kcu.constraint_name
                    WHERE tc.table_schema = 'healthcare'
                      AND tc.table_name = %s
                      AND tc.constraint_type = 'PRIMARY KEY';
                """, (table,))

                primary_keys = [row[0] for row in cur.fetchall()]

                metadata["tables"][table] = {
                    "columns": columns,
                    "primary_keys": primary_keys,
                    "relationships": []
                }

            cur.execute("""
                SELECT
                    tc.table_name AS table_name,
                    kcu.column_name AS column_name,
                    ccu.table_name AS referenced_table,
                    ccu.column_name AS referenced_column
                FROM information_schema.table_constraints AS tc
                JOIN information_schema.key_column_usage AS kcu
                    ON tc.constraint_name = kcu.constraint_name
                    AND tc.table_schema = kcu.table_schema
                JOIN information_schema.constraint_column_usage AS ccu
                    ON tc.constraint_name = ccu.constraint_name
                    AND tc.table_schema = ccu.table_schema
                WHERE tc.constraint_type = 'FOREIGN KEY'
                AND tc.table_schema = 'healthcare'
                ORDER BY tc.table_name, kcu.column_name;
            """)

            for row in cur.fetchall():
                table, column, ref_table, ref_column = row

                metadata["tables"][table]["relationships"].append({
                    "column": column,
                    "references": f"{ref_table}.{ref_column}"
                })

    with open(
        "metadata/database_metadata.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(metadata, f, indent=2)

    print("✓ metadata/database_metadata.json created")


if __name__ == "__main__":
    main()