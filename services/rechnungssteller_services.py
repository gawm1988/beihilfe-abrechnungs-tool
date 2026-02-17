from datenbank.rechnung import read_rechnung
from datenbank.rechnungssteller import read_rechnungssteller_by_name, create_rechnungssteller

def neuen_rechnungsteller_erfassen(name:str, iban:str):
    try:
        rechnungstellerDTO = read_rechnungssteller_by_name(name)
        if rechnungstellerDTO:
            print("Rechnungsteller existiert bereits.")
            return False
    except TypeError as e:
        print(e)
    create_rechnungssteller(name, iban)
    print(f"Rechnungsteller {name} angelegt.")
    return True

def lade_alle_rechnungssteller():
    pass
