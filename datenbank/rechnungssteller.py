from .connection import connect

class RechnungstellerDTO:
    id: int
    name: str
    iban: str

    def __init__(self,id:int, name:str, iban:str):
        self.id = id
        self.name = name
        self.iban = iban


def create_rechnungssteller(name: str, iban: str):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO rechnungssteller (name,iban) VALUES (?,?)", (name, iban))

def read_rechnungssteller_by_name(name: str)->RechnungstellerDTO:
    with connect() as conn:
        cursor = conn.cursor()
        fetch = cursor.execute("SELECT * FROM rechnungssteller WHERE name=?", (name,)).fetchone()
        if fetch is None:
            return None
        return RechnungstellerDTO(fetch[0], fetch[1], fetch[2])

def read_rechnungssteller_by_id(rechnungsteller_id: int)->RechnungstellerDTO:
    with connect() as conn:
        cursor = conn.cursor()
        fetch = cursor.execute("SELECT * FROM rechnungssteller WHERE id=?", (rechnungsteller_id,)).fetchone()
        if fetch is None:
            return None
        return RechnungstellerDTO(fetch[0], fetch[1], fetch[2])

def read_alle_rechnungssteller_namen():
    with connect() as conn:
        cursor = conn.cursor()
        return cursor.execute("SELECT name, iban FROM rechnungssteller").fetchall()

def update_iban(name: str, iban: str):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE rechnungssteller SET iban = ? WHERE name = ?", (iban, name))