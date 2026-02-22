from utils.paths import DB_PATH
from .connection import connect


class PersonDTO:
    id: int
    vorname: str
    nachname: str
    beihilfesatz: float

    def __init__(self, id: int, vorname: str, nachname: str, beihilfesatz: float):
        self.id = id
        self.vorname = vorname
        self.nachname = nachname
        self.beihilfesatz = beihilfesatz

    def __str__(self):
        return f"{self.vorname} {self.nachname}"


def create_person(vorname: str, nachname: str, beihilfesatz: float = 0.0, db_path=DB_PATH):
    with connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO person (vorname,nachname,beihilfesatz) VALUES (?,?,?)",
                       (vorname, nachname, beihilfesatz))


def read_person_by_name(vorname: str, nachname: str, db_path=DB_PATH):
    with connect(db_path) as conn:
        cursor = conn.cursor()
        fetch = cursor.execute("SELECT * FROM person WHERE vorname=? AND nachname=?", (vorname, nachname)).fetchone()
        if fetch is None:
            return None
        return PersonDTO(fetch[0], fetch[1], fetch[2], fetch[3])


def read_person_by_id(person_id: int, db_path=DB_PATH):
    with connect(db_path) as conn:
        cursor = conn.cursor()
        fetch = cursor.execute("SELECT * FROM person WHERE id=?", (person_id,)).fetchone()
        if fetch is None:
            return None
        return PersonDTO(fetch[0], fetch[1], fetch[2], fetch[3])


def read_all_personen(db_path=DB_PATH):
    with connect(db_path) as conn:
        cursor = conn.cursor()
        return cursor.execute("SELECT id, vorname, nachname FROM person").fetchall()
