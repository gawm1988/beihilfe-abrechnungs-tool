from datenbank.person import *

def neue_person_erfassen(vorname: str, nachname: str, beihilfesatz:float = 0.0):
    if not vorname or not nachname:
        print(f"Unvollständige Angaben: {vorname} {nachname}.")
        return False
    try:
        personDTO = read_person_by_name(vorname,nachname)
        if personDTO:
            print(f"Person {vorname} {nachname}  existiert bereits.")
            return False
    except TypeError as e:
        print(e)
    create_person(vorname, nachname, beihilfesatz)
    print(f"Person: {vorname} {nachname} eingefügt.")
    return True

if __name__ == '__main__':
    neue_person_erfassen("Heinz","Müller")