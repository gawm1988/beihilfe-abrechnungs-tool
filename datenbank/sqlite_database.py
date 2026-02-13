import sqlite3
import os

def connect():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DB_PATH = os.path.join(BASE_DIR, "datenbank/beihilfe.db")
    return sqlite3.connect(DB_PATH)


def create_tabellen():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS person (id INTEGER PRIMARY KEY, vorname TEXT NOT NULL, nachname TEXT NOT NULL, beihilfesatz REAL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS leistungsbringer (id INTEGER PRIMARY KEY, name TEXT NOT NULL, iban TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS rechnung (id INTEGER PRIMARY KEY, person_id INTEGER NOT NULL, leistungsbringer_id INTEGER NOT NULL, rechnungsdatum DATE NOT NULL, betrag REAL NOT NULL, verwendungszweck TEXT NOT NULL, abrechnungsdatum DATE)")
    conn.commit()
    conn.close()


def create_person(vorname:str, nachname:str, beihilfesatz:float):
    if vorname == "" or vorname == None or nachname == "" or nachname == None:
        print(f"Unvollständige Angaben: {vorname} {nachname}.")
        return
    if beihilfesatz == None or beihilfesatz == "":
        beihilfesatz = 0.0
    conn = connect()
    cursor = conn.cursor()
    tmp = cursor.execute("SELECT * FROM person WHERE vorname=? AND nachname=?", (vorname,nachname)).fetchone()
    if tmp is None:
        cursor.execute("INSERT INTO person (vorname,nachname,beihilfesatz) VALUES (?,?,?)", (vorname, nachname, beihilfesatz))
        print(f"Person: {vorname} {nachname} eingefügt.")
    else:
        print(f"Person: {vorname} {nachname} existiert bereits.")
    conn.commit()
    conn.close()

def read_person(vorname:str, nachname:str):
    conn = connect()
    cursor = conn.cursor()
    tmp = cursor.execute("SELECT * FROM person WHERE vorname=? AND nachname=?", (vorname,nachname)).fetchone()
    conn.commit()
    conn.close()
    return tmp

def create_leistungserbringer(name:str, iban:str):
    if name == "" or name == None:
        print(f"Unvollständige Angaben: {name}.")
        return
    if iban == None or iban == "":
        iban = "leer"
    if len(iban) <= 22:
        print(f"Hinweis: kurze IBAN: {iban}.")
    conn = connect()
    cursor = conn.cursor()
    tmp = cursor.execute("SELECT * FROM leistungsbringer WHERE name=?", (name,)).fetchone()
    if tmp is None:
        cursor.execute("INSERT INTO leistungsbringer (name,iban) VALUES (?,?)", (name, iban))
        print(f"Leistungsbringer: {name} eingefügt.")
    else:
        print(f"Leistungsbringer: {name} existiert bereits.")
    conn.commit()
    conn.close()

def read_leistungsringer(name:str):
    conn = connect()
    cursor = conn.cursor()
    tmp = cursor.execute("SELECT * FROM leistungsbringer WHERE name=?", (name,)).fetchone()
    conn.commit()
    conn.close()
    return tmp

def update_iban_leistungserbringer(name:str, iban:str):
    if name == "" or name == None:
        print(f"Unvollständige Angaben: {name}.")
        return
    if iban == None or iban == "":
        print(f"Keine IBAN: {iban}.")
        return
    if len(iban) < 22:
        print(f"Hinweis: kurze IBAN: {iban}.")
    conn = connect()
    cursor = conn.cursor()
    try:
        l_exists = read_leistungsringer(name)
        if l_exists is None:
            print(f"Leistungsbringer nicht vorhanden: {name}.")
            return
        cursor.execute("UPDATE leistungsbringer SET iban = ? WHERE name = ?", (iban, name))
        print(f"IBAN aktualisiert: {name} → IBAN: {iban}.")
    except sqlite3.Error as e:
        print(f"Datenbankfehler: {e}")
        conn.rollback()
    finally:
        conn.commit()
        conn.close()

def create_rechnung(person_vorname:str, person_nachname:str, leistungsbringer:str, rechnungsdatum:str, betrag:float, verwendungszweck:str):
    conn = connect()
    cursor = conn.cursor()
    try:
        p_exists = read_person(person_vorname,person_nachname)
        if p_exists is None:
            print(f"Person nicht vorhanden: {person_vorname} {person_nachname}.")
            return
        person_id = p_exists[0]

        l_exists = read_leistungsringer(leistungsbringer)
        if l_exists is None:
            print(f"Leistungsbringer nicht vorhanden: {leistungsbringer}.")
            return
        leistungsbringer_id = l_exists[0]

        tmp = cursor.execute("SELECT * FROM rechnung WHERE person_id=? AND leistungsbringer_id=? AND rechnungsdatum=?", (person_id,leistungsbringer_id,rechnungsdatum)).fetchone()
        if tmp == None:
            cursor.execute("INSERT INTO rechnung (person_id,leistungsbringer_id,rechnungsdatum,betrag,verwendungszweck) VALUES (?,?,?,?,?)",(person_id,leistungsbringer_id,rechnungsdatum,betrag,verwendungszweck))
            print(f"Rechnung eingefügt: {person_vorname} {person_nachname} → {leistungsbringer}: {betrag}, {verwendungszweck} vom {rechnungsdatum}.")
            return
        print(f"Rechnung existiert bereits: {person_vorname} {person_nachname} → {leistungsbringer}: {verwendungszweck} vom {rechnungsdatum}.")
    except sqlite3.Error as e:
        print(f"Datenbankfehler: {e}")
        conn.rollback()
    finally:
        conn.commit()
        conn.close()

def read_offene_rechnungen(person_vorname:str, person_nachname:str):
    conn = connect()
    cursor = conn.cursor()
    try:
        p_exists = read_person(person_vorname,person_nachname)
        if p_exists is None:
            print(f"Person nicht vorhanden: {person_vorname} {person_nachname}.")
            return
        person_id = p_exists[0]
        rechnungen = cursor.execute("SELECT * FROM rechnung WHERE person_id=? AND abrechnungsdatum IS NULL", (person_id,)).fetchall()
        print(rechnungen)
    except sqlite3.Error as e:
        print(f"Datenbankfehler: {e}")
        conn.rollback()
    finally:
        conn.commit()
        conn.close()
    return rechnungen

def update_datum_rechnungen(person_vorname:str, person_nachname:str, datum:str):
    conn = connect()
    cursor = conn.cursor()
    try:
        p_exists = read_person(person_vorname, person_nachname)
        if p_exists is None:
            print(f"Person nicht vorhanden: {person_vorname} {person_nachname}.")
            return
        person_id = p_exists[0]

        rechnungen = read_offene_rechnungen(person_vorname,person_nachname)
        if rechnungen is None:
            print(f"Keine offenen Rechnungen für {person_vorname} {person_nachname}.")
            return
        cursor.execute("UPDATE rechnung SET abrechnungsdatum=? WHERE abrechnungsdatum IS NULL AND person_id=?", (datum,person_id))
    except sqlite3.Error as e:
        print(f"Datenbankfehler: {e}")
        conn.rollback()
    finally:
        conn.commit()
        conn.close()


if __name__ == '__main__':
    #create_tabellen()
    #create_person("Max","Mustermann",0.7)
    #create_leistungserbringer("Test","DE12123456789012345678")
    #create_rechnung("Max","Mustermann","Test","01.01.2026",10.21,"12345")
    print(read_person("Max","Mustermann"))