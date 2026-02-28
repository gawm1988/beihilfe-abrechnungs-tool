from .connection import connect


class RechnungDTO:
    id: int
    person_id: int
    rechnungssteller_id: int
    rechnungsdatum: str
    betrag: str
    verwendungszweck: str
    hashwert: str
    abrechnung_id: int

    def __init__(self, id: int, person_id: int, rechnungsteller_id: int, rechnungsdatum: str, betrag: str,
                 verwendungszweck: str, hashwert: str, abrechnung_id:int):
        self.id = id
        self.person_id = person_id
        self.rechnungssteller_id = rechnungsteller_id
        self.rechnungsdatum = rechnungsdatum
        self.betrag = betrag
        self.verwendungszweck = verwendungszweck
        self.hashwert = hashwert
        self.abrechnung_id = abrechnung_id

    def __str__(self):
        return f"{self.person_id} → {self.rechnungssteller_id}:\n€ {self.betrag}\nVWZ: {self.verwendungszweck}\nvom {self.rechnungsdatum}\n"


def create_rechnung(db_path:str, person_id: int, rechnungssteller_id: int, rechnungsdatum: str, betrag: float, verwendungszweck: str,
                    ) -> bool:
    with connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO rechnung (person_id,rechnungssteller_id,rechnungsdatum,betrag,verwendungszweck) VALUES (?,?,?,?,?) RETURNING *",
            (person_id, rechnungssteller_id, rechnungsdatum, betrag, verwendungszweck)
        )
        return RechnungDTO(*cursor.fetchone())


def read_rechnung(db_path:str, person_id: int, rechnungssteller_id: int, rechnungsdatum: str, betrag: float, verwendungszweck: str,
                  ):
    with connect(db_path) as conn:
        cursor = conn.cursor()
        fetch = cursor.execute(
            "SELECT * FROM rechnung WHERE person_id=? AND rechnungssteller_id=? AND rechnungsdatum=? AND betrag=? AND verwendungszweck=?",
            (person_id, rechnungssteller_id, rechnungsdatum, betrag, verwendungszweck)).fetchone()
        if fetch is None:
            return None
        print(*fetch)
        return RechnungDTO(*fetch)


def read_rechnung_by_id(db_path:str, rechnung_id: int):
    with connect(db_path) as conn:
        cursor = conn.cursor()
        fetch = cursor.execute(
            "SELECT * FROM rechnung WHERE id=?",
            (rechnung_id,)).fetchone()
        if fetch is None:
            return None
        return RechnungDTO(*fetch)


def read_offene_rechnungen_von_person_id(db_path:str, person_id: int):
    with connect(db_path) as conn:
        cursor = conn.cursor()
        rechnungen = []
        fetch = cursor.execute(
            "SELECT * FROM rechnung WHERE person_id=? AND abrechnung_id IS NULL",
            (person_id,)
        ).fetchall()
        if fetch is None:
            return None
        for f in fetch:
            rechnungen.append(RechnungDTO(*f))
        return rechnungen


def update_abrechnung_id(db_path:str, person_id: int, abrechnung_id: int):
    with connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE rechnung SET abrechnung_id=? WHERE person_id=? AND abrechnung_id IS NULL RETURNING *",
            (abrechnung_id, person_id)
        )
        return RechnungDTO(*cursor.fetchone())

def read_rechnungen_by_abrechnung_id(db_path:str, abrechnung_id: int):
    with connect(db_path) as conn:
        cursor = conn.cursor()
        fetch = cursor.execute(
            "SELECT * FROM rechnung WHERE abrechnung_id=?",
            (abrechnung_id,)
        ).fetchall()
        if fetch is None:
            return None
        rechnungen = []
        for f in fetch:
            rechnungen.append(RechnungDTO(*f))
        return rechnungen


def update_hashwert(db_path:str, rechnung_id: int, hashwert: str):
    with connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE rechnung SET hashwert=? WHERE id=? RETURNING *",
            (hashwert, rechnung_id)
        )
        return RechnungDTO(*cursor.fetchone())

def read_rechnung_by_id_person_rechnungssteller(db_path:str, person_id:int, rechnungssteller_id:int, rechnungsdatum:str):
    with connect(db_path) as conn:
        cursor = conn.cursor()
        fetch = cursor.execute(
            "SELECT * FROM rechnung WHERE person_id=? AND rechnungssteller_id=? AND rechnungsdatum=?",(person_id, rechnungssteller_id,rechnungsdatum)
        ).fetchone()
        if fetch is None:
            return None
        return RechnungDTO(*fetch)
    
def read_rechnung_by_hashwert(db_path:str, hashwert:str):
    with connect(db_path) as conn:
        cursor = conn.cursor()
        fetch = cursor.execute(
            "SELECT * FROM rechnung WHERE hashwert=?",
            (hashwert,)
        ).fetchone()
        if fetch is None:
            return None
        return RechnungDTO(*fetch)