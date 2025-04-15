# db_manager.py

import psycopg2
import os
from dotenv import load_dotenv
from contextlib import contextmanager

load_dotenv()

from prefect import flow, task


@task(log_prints=True)
@contextmanager
def get_db_connection():
    conn = None
    try:
        conn = psycopg2.connect(
            user=os.getenv("USER"),
            password=os.getenv("POSTGRES_PASS"),
            host=os.getenv("HOST"),
            port=os.getenv("PORT"),
            dbname=os.getenv("DBNAME")
        )
        cursor = conn.cursor()
        print("✅ Database connection established.")
        yield conn, cursor
    except Exception as e:
        print("❌ Failed to connect to the database:", e)
        yield None, None
    finally:
        if conn:
            conn.close()
            print("🔒 Connection closed.")


@task(log_prints=True)
def execute_query(query, params=None, fetch=False):
    with get_db_connection() as (conn, cursor):
        if cursor:
            try:
                cursor.execute(query, params)
                if fetch:
                    return cursor.fetchall()
                else:
                    conn.commit()  # Commit only if not fetching
                    return True
            except Exception as e:
                return "❌ Error executing query:", e
        return None
