import psycopg


DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "mcp_sql_agent",
    "user": "postgres",
    "password": "YourPasswordHere"
}


def main():
    with psycopg.connect(**DB_CONFIG) as conn:

        with conn.cursor() as cursor:
            cursor.execute("SELECT version();")

            version = cursor.fetchone()[0]

            print("Connected to PostgreSQL!")
            print(version)


if __name__ == "__main__":
    main()