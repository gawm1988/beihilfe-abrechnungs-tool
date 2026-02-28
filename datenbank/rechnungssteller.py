from .connection import connect


class RechnungstellerDTO:
    id: int
    name: str
    iban: str

    def __init__(self, id: int, name: str, iban: str):
        self.id = id
        self.name = name
        self.iban = iban

    def __str__(self):
        return f"{self.name}"


def create_rechnungssteller(db_path:str, name: str, iban: str):
    with connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO rechnungssteller (name,iban) VALUES (?,?) RETURNING *",
            (name, iban))
        return RechnungstellerDTO(*cursor.fetchone())


def read_rechnungssteller_by_name(db_path:str, name: str) -> RechnungstellerDTO:
    with connect(db_path) as conn:
        cursor = conn.cursor()
        fetch = cursor.execute("SELECT * FROM rechnungssteller WHERE name=?", (name,)).fetchone()
        if fetch is None:
            return None
        return RechnungstellerDTO(*fetch)


def read_rechnungssteller_by_id(db_path:str, rechnungsteller_id: int) -> RechnungstellerDTO:
    with connect(db_path) as conn:
        cursor = conn.cursor()
        fetch = cursor.execute("SELECT * FROM rechnungssteller WHERE id=?", (rechnungsteller_id,)).fetchone()
        if fetch is None:
            return None
        return RechnungstellerDTO(*fetch)

def read_alle_rechnungssteller(db_path):
    with connect(db_path) as conn:
        cursor = conn.cursor()
        rechnungssteller = cursor.execute("SELECT * FROM rechnungssteller").fetchall()
        if not rechnungssteller:
            return None
        rechnungstellerDTO_list = []
        for r in rechnungssteller:
            rechnungstellerDTO_list.append(RechnungstellerDTO(*r))
        return rechnungstellerDTO_list

def update_iban(db_path:str, name: str, iban: str):
    with connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE rechnungssteller SET iban = ? WHERE name = ? RETURNING *", (iban, name))
        return RechnungstellerDTO(*cursor.fetchone())
