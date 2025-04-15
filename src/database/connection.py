# db_manager.py

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                user=os.getenv("USER"),
                password=os.getenv("POSTGRES_PASS"),
                host=os.getenv("HOST"),
                port=os.getenv("PORT"),
                dbname=os.getenv("DBNAME")
            )
            self.cursor = self.connection.cursor()
            print("✅ Database connection established.")
        except Exception as e:
            print("❌ Failed to connect to the database:", e)
            self.connection = None
            self.cursor = None

    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Exception as e:
            print("❌ Error executing query:", e)
            return None

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("🔒 Connection closed.")
