# db_manager.py

import psycopg2
import os
from contextlib import contextmanager
from dotenv import load_dotenv
import logging

logging.basicConfig(
    level=logging.INFO,
)

import traceback
#"/secrets/x-startup-secrets"
try:
    load_dotenv("/secrets/x-startup-secrets")
except Exception as e:
    print("❌ Failed to load .env secret:", e)

@contextmanager
def get_db_connection():
    conn = None

    try:
        conn = psycopg2.connect(
            user=os.getenv("USER"),
            password=os.getenv("POSTGRES_PASS"),
            host=os.getenv("HOST"),
            port='6543',
            dbname=os.getenv("DBNAME"),
            sslmode='require'
        )
        cursor = conn.cursor()
        logging.info("✅ Database connection established.")
        yield conn, cursor
    except Exception as e:
        logging.error("❌ Failed to connect to the database:", e)
        logging.error(traceback.format_exc())
        yield None, None
    finally:
        if conn:
            conn.close()
            logging.info("🔒 Connection closed.")



def execute_query(query, params=None, fetch=False):
    with get_db_connection() as (conn, cursor):
        if cursor:
            try:
                cursor.execute(query, params)
                if fetch:
                    result = cursor.fetchall()
                    logging.info("✅ Query executed (with fetch): %s", query)
                    return result
                else:
                    conn.commit()
                    logging.info("✅ Query executed (commit): %s", query)
                    return True
            except Exception as e:
                return "❌ Error executing query:", e
        return None

