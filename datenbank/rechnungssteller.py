from .connection import connect

class RechnungstellerDTO:
    id: int
    name: str
    iban: str

    def __init__(self,id:int, name:str, iban:str):
        self.id = id
        self.name = name
        self.iban = iban


def create_rechnungssteller(name: str, iban: str = "leer"):
    if not name:
        print(f"Unvollständige Angaben: {name}.")
        return
    if len(iban) < 22:
        print(f"Hinweis: kurze IBAN: {iban}.")

    with connect() as conn:
        cursor = conn.cursor()
        tmp = cursor.execute("SELECT * FROM rechnungssteller WHERE name=?", (name,)).fetchone()
        if tmp is None:
            cursor.execute("INSERT INTO rechnungssteller (name,iban) VALUES (?,?)", (name, iban))
            print(f"Rechnungssteller: {name} eingefügt.")
        else:
            print(f"Rechnungssteller: {name} existiert bereits.")

def read_rechnungssteller(name: str):
    with connect() as conn:
        cursor = conn.cursor()
        fetch = cursor.execute("SELECT * FROM rechnungssteller WHERE name=?", (name,)).fetchone()
        return RechnungstellerDTO(fetch[0], fetch[1], fetch[2])

def read_rechnungssteller_by_id(rechnungsteller_id: int)->RechnungstellerDTO:
    with connect() as conn:
        cursor = conn.cursor()
        fetch = cursor.execute("SELECT * FROM rechnungssteller WHERE id=?", (rechnungsteller_id,)).fetchone()
        return RechnungstellerDTO(fetch[0], fetch[1], fetch[2])

def read_all_rechnungssteller():
    with connect() as conn:
        cursor = conn.cursor()
        return cursor.execute("SELECT id, name FROM rechnungssteller").fetchall()

def update_iban(name: str, iban: str):
    if not name or not iban:
        print("Unvollständige Angaben.")
        return
    if len(iban) < 22:
        print(f"Hinweis: kurze IBAN: {iban}.")

    with connect() as conn:
        cursor = conn.cursor()
        l_exists = read_leistungsbringer(name)
        if l_exists is None:
            print(f"Rechnungssteller nicht vorhanden: {name}.")
            return
        cursor.execute("UPDATE rechnungssteller SET iban = ? WHERE name = ?", (iban, name))
        print(f"IBAN aktualisiert: {name} → {iban}.")
