import json
import os
import re

import psycopg
from dotenv import load_dotenv
# from openai import OpenAI
import ollama
from mcp.server.mcpserver import MCPServer

load_dotenv()

mcp = MCPServer("mcp-sql-agent")

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

METADATA_FILE = "metadata/database_metadata.json"


def load_metadata():
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def clean_sql(sql: str) -> str:
    sql = sql.strip()

    if sql.startswith("```"):
        sql = re.sub(r"```(?:sql)?", "", sql, flags=re.IGNORECASE)
        sql = sql.replace("```", "").strip()

    return sql.rstrip(";").strip()


def validate_sql(sql: str):
    sql = clean_sql(sql)

    if not re.match(r"^(SELECT|WITH)\b", sql, re.IGNORECASE):
        raise ValueError("Only SELECT/WITH queries are allowed.")

    forbidden = [
        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "ALTER",
        "TRUNCATE",
        "CREATE",
        "GRANT",
        "REVOKE",
        "COPY",
    ]

    for keyword in forbidden:
        if re.search(rf"\b{keyword}\b", sql, re.IGNORECASE):
            raise ValueError(f"Forbidden SQL operation: {keyword}")

    if ";" in sql:
        raise ValueError("Multiple SQL statements are not allowed.")

    return sql


def generate_sql(question: str, error: str | None = None, previous_sql: str | None = None):
    metadata = load_metadata()

    prompt = f"""
                You are a PostgreSQL SQL generator.

                Database metadata:
                {json.dumps(metadata, indent=2)}

                User request:
                {question}

                Generate ONE read-only PostgreSQL query based on the user request.

                Rules:
                - Use only tables and columns present in the metadata.
                - Use actual relationships from metadata for JOINs.
                - Only SELECT or WITH queries.
                - Never INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE or other write operations.
                - Return ONLY SQL.

                """

    if error:
        prompt += f"""
                    Previous SQL:
                    {previous_sql}

                    Database error:
                    {error}

                    Correct the SQL using the metadata.
                    Return ONLY the corrected SQL.
                    """

    response = ollama.chat(
            model="qwen2.5-coder:7b",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
    
    return response['message']['content'].strip()


@mcp.tool()
def generate_query(user_question: str) -> str:
    """Generate a read-only PostgreSQL query from a natural-language request."""

    sql = generate_sql(user_question)

    validate_sql(sql)

    return sql


@mcp.tool()
def execute_query(sql: str) -> str:
    """Validate and execute a read-only PostgreSQL query."""

    sql = validate_sql(sql)

    max_retries = 2
    last_error = None

    for attempt in range(max_retries + 1):

        try:
            with psycopg.connect(**DB_CONFIG) as conn:
                with conn.cursor() as cur:

                    cur.execute("SET search_path TO healthcare;")
                    cur.execute(sql)

                    rows = cur.fetchall()
                    columns = [
                        desc.name
                        for desc in cur.description
                    ]

                    return json.dumps(
                        {
                            "success": True,
                            "row_count": len(rows),
                            "columns": columns,
                            "data": rows,
                        },
                        default=str
                    )

        except Exception as exc:

            last_error = str(exc)

            if attempt == max_retries:
                break

            sql = generate_sql(
                question="Fix the previous SQL query.",
                error=last_error,
                previous_sql=sql
            )

            validate_sql(sql)

    return json.dumps(
        {
            "success": False,
            "error": last_error,
            "message": "Query failed after retries."
        }
    )


if __name__ == "__main__":
    mcp.run()