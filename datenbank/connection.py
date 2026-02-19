import sqlite3
import os

from utils.paths import DB_PATH

def connect():
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
                pdf_path TEXT,
                abrechnungsdatum DATE
            )
        """)
