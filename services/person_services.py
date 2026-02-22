import re

from datenbank.person import *
from utils.paths import DB_PATH

def neue_person_erfassen(vorname: str, nachname: str, beihilfesatz: str, db_path=DB_PATH):
    if not ist_gueltiger_beihilfesatz(beihilfesatz):
        return False, "Ungültiger Beihilfesatz\n Format: 0,8 oder 0.75"
    beihilfesatz = float(beihilfesatz.replace(",", "."))
    if not vorname or not nachname:
        return False, "Unvollständige Angaben"
    personDTO = read_person_by_name(db_path,vorname, nachname)
    if personDTO:
        return False, f"Person {vorname} {nachname} existiert bereits."
    create_person(db_path, vorname, nachname, beihilfesatz)
    return True, f"Person: {vorname} {nachname} eingefügt."


def ist_gueltiger_beihilfesatz(s: str) -> bool:
    pattern = r"^0[.,]\d{1,2}$"
    return re.fullmatch(pattern, s) is not None


if __name__ == '__main__':
    neue_person_erfassen("Heinz", "Müller")
