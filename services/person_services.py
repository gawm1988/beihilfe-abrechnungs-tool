from datenbank.person import *
import re


def neue_person_erfassen(vorname: str, nachname: str, beihilfesatz: str):
    if not ist_gueltiger_beihilfesatz(beihilfesatz):
        return False, "Ungültiger Beihilfesatz\n Format: 0,8 oder 0.75"
    beihilfesatz = float(beihilfesatz.replace(",", "."))
    if not vorname or not nachname:
        return False, "Unvollständige Angaben"
    personDTO = read_person_by_name(vorname, nachname)
    if personDTO:
        return False, f"Person {vorname} {nachname} existiert bereits."
    create_person(vorname, nachname, beihilfesatz)
    return True, f"Person: {vorname} {nachname} eingefügt."

if __name__ == '__main__':
    neue_person_erfassen("Heinz", "Müller")

def ist_gueltiger_beihilfesatz(s: str) -> bool:
    pattern = r"^0[.,]\d{1,2}$"
    return re.fullmatch(pattern, s) is not None