from .connection import connect

class PersonDTO:
    id:int
    vorname:str
    nachname:str
    beihilfesatz:float

    def __init__(self, id:int, vorname:str, nachname:str, beihilfesatz:float):
        self.id = id
        self.vorname = vorname
        self.nachname = nachname
        self.beihilfesatz = beihilfesatz


def create_person(vorname: str, nachname: str, beihilfesatz: float = 0.0):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO person (vorname,nachname,beihilfesatz) VALUES (?,?,?)",(vorname, nachname, beihilfesatz))

def read_person_by_name(vorname: str, nachname: str):
    with connect() as conn:
        cursor = conn.cursor()
        fetch = cursor.execute("SELECT * FROM person WHERE vorname=? AND nachname=?",(vorname, nachname)).fetchone()
        return PersonDTO(fetch[0], fetch[1], fetch[2], fetch[3])

def read_all_personen():
    with connect() as conn:
        cursor = conn.cursor()
        return cursor.execute("SELECT id, vorname, nachname FROM person").fetchall()
