from .connection import connect

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

    def __str__(self):
        return f"{self.person_id} → {self.rechnungssteller_id}:\n€ {self.betrag}\nVWZ: {self.verwendungszweck}\nvom {self.rechnungsdatum}\n"

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
        if fetch is None:
            return None
        return RechnungDTO(fetch[0], fetch[1], fetch[2], fetch[3], fetch[4], fetch[5])

def read_offene_rechnungen_von_person_id(person_id: int):
    with connect() as conn:
        cursor = conn.cursor()
        rechnungen = []
        fetch = cursor.execute(
            "SELECT * FROM rechnung WHERE person_id=? AND abrechnungsdatum IS NULL",
            (person_id,)
        ).fetchall()
        if fetch is None:
            return None
        for f in fetch:
            rechnungen.append(RechnungDTO(f[0], f[1], f[2], f[3], f[4], f[5]))
        return rechnungen

def update_abrechnungsdatum(rechnung_id: int, abrechnungsdatum:str):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE rechnung SET abrechnungsdatum=? WHERE id=?",
            (abrechnungsdatum,rechnung_id)
        )
