import collections
from datenbank.rechnung import read_rechnung
from datenbank.rechnungssteller import read_rechnungssteller_by_name, create_rechnungssteller, \
    read_alle_rechnungssteller_namen, update_iban
from schwifty import IBAN

def ist_valide_iban(iban:str):
    if iban == "":
        return True
    try:
        iban = IBAN(iban)
        print("IBAN ist gültig")
        return True
    except ValueError:
        print("IBAN ist ungültig")
        return False


def neuen_rechnungsteller_erfassen(name:str, iban:str):
    try:
        rechnungstellerDTO = read_rechnungssteller_by_name(name)
        if rechnungstellerDTO:
            return False, "Rechnungsteller existiert bereits."
    except TypeError as e:
        print(e)
    if ist_valide_iban(iban):
        create_rechnungssteller(name, iban)
        return True, f"Rechnungsteller {name} angelegt.\nIBAN: {iban}"
    else:
        return False, f"IBAN {iban} ist ungültig."

def lade_alle_rechnungssteller()->dict[str, int]:
    try:
        rechnungssteller = read_alle_rechnungssteller_namen()
        rechnungssteller_dict = {
            f"{name}": iban
            for name, iban in rechnungssteller
        }
        return collections.OrderedDict(sorted(rechnungssteller_dict.items()))
    except TypeError as e:
        print(e)
        return None

def iban_aktualisieren(name:str, iban:str):
    if not ist_valide_iban(iban):
        return False, f"IBAN {iban} ist ungültig."
    try:
        read_rechnungssteller_by_name(name)
        update_iban(name, iban)
        return True, f"Rechnungsteller {name} aktualisiert.\nIBAN: {iban}"
    except TypeError as e:
        print(e)
        return False, f"Rechnungsteller existiert nicht."


if __name__ == '__main__':
    #print(ist_valide_iban("GB33BUKB20201555555555"))
    iban_aktualisieren("A","GB33BUKB20201555555555")