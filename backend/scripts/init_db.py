import os

import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

load_dotenv()

# Database configuration
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_NAME = os.getenv("POSTGRES_DB", "transrom")


def init_database():
    try:
        # Connect to PostgreSQL server
        conn = psycopg2.connect(
            user=DB_USER, password=DB_PASSWORD, host=DB_HOST, database="postgres"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # Check if database exists
        cursor.execute(
            f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{DB_NAME}'"
        )
        exists = cursor.fetchone()

        if not exists:
            # Create database
            print(f"Creating database {DB_NAME}...")
            cursor.execute(f'CREATE DATABASE "{DB_NAME}"')
            print(f"Database {DB_NAME} created successfully!")
        else:
            print(f"Database {DB_NAME} already exists.")

        cursor.close()
        conn.close()

        print("Database initialization completed successfully!")
        return True

    except Exception as e:
        print(f"An error occurred: {e}")
        return False


if __name__ == "__main__":
    init_database()
