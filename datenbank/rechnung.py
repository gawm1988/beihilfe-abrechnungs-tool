from .connection import connect
from .person import read_person_by_name

class RechnungDTO:
    id: int
    person_id:int
    rechnungssteller_id: int
    rechnungsdatum: str
    betrag: str
    verwendungszweck: str
    abrechnungsdatum: str

    def __init__(self, id:int, person_id:int, rechnungsteller_id:int, rechnungsdatum:str, betrag:str, verwendungszweck:str):
        self.id = id
        self.person_id = person_id
        self.rechnungssteller_id = rechnungsteller_id
        self.rechnungsdatum = rechnungsdatum
        self.betrag = betrag
        self.verwendungszweck = verwendungszweck


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
        fetch = cursor.execute("SELECT * FROM rechnung WHERE person_id=? AND rechnungssteller_id=? AND rechnungsdatum=? AND betrag=? AND verwendungszweck=?", (person_id,rechnungssteller_id,rechnungsdatum,betrag,verwendungszweck)).fetchone()
        return RechnungDTO(fetch[0], fetch[1], fetch[2], fetch[3], fetch[4], fetch[5])

def read_offene_rechnungen(person_vorname: str, person_nachname: str):
    person = read_person_by_name(person_vorname, person_nachname)
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

    person = read_person_by_name(person_vorname, person_nachname)
    person_id = person[0]

    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE rechnung SET abrechnungsdatum=? WHERE person_id=? AND abrechnungsdatum IS NULL",
            (datum, person_id)
        )
        print(f"Abrechnungsdatum aktualisiert auf {datum} für {person_vorname} {person_nachname}.")
