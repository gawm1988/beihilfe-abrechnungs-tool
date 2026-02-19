import sqlite3
import os

DATABASE_NAME = "beihilfe.db"

def connect(database_name: str = DATABASE_NAME):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DB_PATH = os.path.join(BASE_DIR, f"datenbank/{database_name}")
    return sqlite3.connect(DB_PATH)


def create_tabellen():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS person (
                id INTEGER PRIMARY KEY, 
                vorname TEXT NOT NULL, 
                nachname TEXT NOT NULL, 
                beihilfesatz REAL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rechnungssteller (
                id INTEGER PRIMARY KEY, 
                name TEXT NOT NULL, 
                iban TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rechnung (
                id INTEGER PRIMARY KEY,
                person_id INTEGER NOT NULL,
                rechnungssteller_id INTEGER NOT NULL,
                rechnungsdatum DATE NOT NULL,
                betrag REAL NOT NULL,
                verwendungszweck TEXT NOT NULL,
                abrechnungsdatum DATE
            )
        """)
