from .connection import connect
from .person import read_person

def create_rechnung(person_id: int, rechnungssteller_id: int, rechnungsdatum: str, betrag: float, verwendungszweck: str) -> bool:
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO rechnung (person_id,rechnungssteller_id,rechnungsdatum,betrag,verwendungszweck) VALUES (?,?,?,?,?)",
            (person_id, rechnungssteller_id, rechnungsdatum, betrag, verwendungszweck)
        )

def read_rechnung(person_id: int, rechnungssteller_id: int, rechnungsdatum: str, betrag: float, verwendungszweck: str):
    with connect() as conn:
        cursor = conn.cursor()
        return cursor.execute("SELECT * FROM rechnung WHERE person_id=? AND rechnungssteller_id=? AND rechnungsdatum=? AND betrag=? AND verwendungszweck=?", (person_id,rechnungssteller_id,rechnungsdatum,betrag,verwendungszweck)).fetchone()

def read_offene_rechnungen(person_vorname: str, person_nachname: str):
    person = read_person(person_vorname, person_nachname)
    if not person:
        print(f"Person nicht vorhanden: {person_vorname} {person_nachname}.")
        return []

    person_id = person[0]
    with connect() as conn:
        cursor = conn.cursor()
        return cursor.execute(
            "SELECT * FROM rechnung WHERE person_id=? AND abrechnungsdatum IS NULL",
            (person_id,)
        ).fetchall()

def update_datum_rechnungen(person_vorname: str, person_nachname: str, datum: str):
    rechnungen = read_offene_rechnungen(person_vorname, person_nachname)
    if not rechnungen:
        print(f"Keine offenen Rechnungen für {person_vorname} {person_nachname}.")
        return

    person = read_person(person_vorname, person_nachname)
    person_id = person[0]

    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE rechnung SET abrechnungsdatum=? WHERE person_id=? AND abrechnungsdatum IS NULL",
            (datum, person_id)
        )
        print(f"Abrechnungsdatum aktualisiert auf {datum} für {person_vorname} {person_nachname}.")
