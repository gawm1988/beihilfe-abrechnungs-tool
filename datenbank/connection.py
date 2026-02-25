import sqlite3

def connect(db_path:str):
    return sqlite3.connect(db_path)


def create_tabellen(db_path:str):
    with connect(db_path) as conn:
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
                hashwert TEXT,
                abrechnung_id INTEGER
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS abrechnung (
                id INTEGER PRIMARY KEY,
                abrechnungsdatum DATE NOT NULL,
                gesamtbetrag REAL NOT NULL,
                beihilfebetrag REAL,
                pkv_betrag REAL,
                hashwert TEXT                
            )
        """)
