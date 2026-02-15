from .connection import connect

def create_person(vorname: str, nachname: str, beihilfesatz: float = 0.0):
    if not vorname or not nachname:
        print(f"Unvollständige Angaben: {vorname} {nachname}.")
        return

    with connect() as conn:
        cursor = conn.cursor()
        tmp = cursor.execute(
            "SELECT * FROM person WHERE vorname=? AND nachname=?",
            (vorname, nachname)
        ).fetchone()
        if tmp is None:
            cursor.execute(
                "INSERT INTO person (vorname,nachname,beihilfesatz) VALUES (?,?,?)",
                (vorname, nachname, beihilfesatz)
            )
            print(f"Person: {vorname} {nachname} eingefügt.")
        else:
            print(f"Person: {vorname} {nachname} existiert bereits.")

def read_person(vorname: str, nachname: str):
    with connect() as conn:
        cursor = conn.cursor()
        return cursor.execute(
            "SELECT * FROM person WHERE vorname=? AND nachname=?",
            (vorname, nachname)
        ).fetchone()

def read_all_personen():
    with connect() as conn:
        cursor = conn.cursor()
        return cursor.execute("SELECT id, vorname, nachname FROM person").fetchall()
