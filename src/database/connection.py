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


@contextmanager
def get_db_connection():
    # "/secrets/x-startup-secrets"
    try:
        load_dotenv("/secrets/x-startup-secrets")
    except Exception as e:
        print("❌ Failed to load .env secret:", e)

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


@contextmanager
def get_db_connection_local():
    try:
        load_dotenv()
    except Exception as e:
        print("❌ Failed to load .env secret:", e)

    conn = None
    print("❌ Loading local secrets from .env file")

    try:
        conn = psycopg2.connect(
            user=os.getenv("USER_LOCAL"),
            password=os.getenv("POSTGRES_PASS"),
            host=os.getenv("HOST_LOCAL"),
            port='5432',
            dbname=os.getenv("DBNAME_LOCAL"),
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
