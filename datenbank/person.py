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


def create_person(db_path: str, vorname: str, nachname: str, beihilfesatz: float = 0.0):
    with connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO person (vorname,nachname,beihilfesatz) VALUES (?,?,?) RETURNING *",
                       (vorname, nachname, beihilfesatz))
        return PersonDTO(*cursor.fetchone())


def read_person_by_name(db_path: str, vorname: str, nachname: str):
    with connect(db_path) as conn:
        cursor = conn.cursor()
        fetch = cursor.execute("SELECT * FROM person WHERE vorname=? AND nachname=?", (vorname, nachname)).fetchone()
        if fetch is None:
            return None
        return PersonDTO(*fetch)


def read_person_by_id(db_path: str, person_id: int):
    with connect(db_path) as conn:
        cursor = conn.cursor()
        fetch = cursor.execute("SELECT * FROM person WHERE id=?", (person_id,)).fetchone()
        if fetch is None:
            return None
        return PersonDTO(*fetch)


def read_all_personen(db_path: str):
    with connect(db_path) as conn:
        cursor = conn.cursor()
        personen = cursor.execute("SELECT * FROM person").fetchall()
        if not personen:
            return None
        personenDTO_list = []
        for p in personen:
            personenDTO_list.append(PersonDTO(*p))
        return personenDTO_list