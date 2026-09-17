import os
import glob
import json

import pandas as pd
from dotenv import load_dotenv
import ollama

load_dotenv()

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# MODEL = "gpt-5.6-luna"


def generate_migration(table_name, columns):
    prompt = f"""
Generate a PostgreSQL CREATE TABLE statement.

Table: {table_name}

Columns:
{json.dumps(columns, indent=2)}

Rules:
- Infer appropriate PostgreSQL data types.
- Use the first column as the primary key.
- Include relationhips based on *_id columns.
- Return ONLY SQL.
- Do not include markdown fences.
- Do not include INSERT , DROP , UPDATE , DELETE statements.
"""

    response = ollama.chat(
        model="qwen2.5-coder:7b",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response['message']['content'].strip()


def main():
    os.makedirs("migrations", exist_ok=True)

    for file in glob.glob("data/*.csv"):
        table_name = os.path.splitext(os.path.basename(file))[0]

        df = pd.read_csv(file, nrows=100)

        columns = [
            {
                "name": column,
                "pandas_type": str(df[column].dtype)
            }
            for column in df.columns
        ]

        print(f"Generating migration for {table_name}...")

        sql = generate_migration(table_name, columns)

        output_file = f"migrations/{table_name}.sql"

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(sql + "\n")

        print(f"✓ {output_file}")


if __name__ == "__main__":
    main()