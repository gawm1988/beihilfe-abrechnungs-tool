import collections

from schwifty import IBAN

from datenbank.rechnungssteller import *
from utils.paths import DB_PATH



def ist_valide_iban(iban: str):
    if iban == "":
        return True
    try:
        iban = IBAN(iban)
        return True
    except ValueError:
        return False


def neuen_rechnungsteller_erfassen(name: str, iban: str, db_path = DB_PATH) -> (bool, str):
    rechnungstellerDTO = read_rechnungssteller_by_name(db_path,name)
    if rechnungstellerDTO:
        return False, "Rechnungssteller existiert bereits."

    if not ist_valide_iban(iban):
        return False, f"IBAN {iban} ist ungültig."

    create_rechnungssteller(db_path, name, iban)
    return True, f"Rechnungssteller {name} angelegt.\nIBAN: {iban}"


def lade_alle_rechnungssteller_iban_dict(db_path=DB_PATH) -> dict[str, str]:
    rechnungsstellerDTO_list = read_alle_rechnungssteller(db_path)
    if not rechnungsstellerDTO_list:
        return None
    rechnungssteller_dict = {
        r.name: r.iban
        for r in rechnungsstellerDTO_list
    }
    return collections.OrderedDict(sorted(rechnungssteller_dict.items()))


def lade_alle_rechnungssteller_dict(db_path=DB_PATH) -> dict[int, str]:
    rechnungsstellerDTO_list = read_alle_rechnungssteller(db_path)
    if not rechnungsstellerDTO_list:
        return None
    return {
        r.id: r.name
        for r in rechnungsstellerDTO_list
    }


def iban_aktualisieren(name: str, iban: str, db_path=DB_PATH) -> (bool, str):
    if not ist_valide_iban(iban):
        return False, f"IBAN {iban} ist ungültig."

    rechnungstellerDTO = read_rechnungssteller_by_name(db_path,name)
    if not rechnungstellerDTO:
        return False, f"Rechnungssteller {name} existiert nicht."

    update_iban(db_path, name, iban)
    return True, f"Rechnungssteller {name} aktualisiert.\nIBAN: {iban}"

def lade_iban(rechnungsteller_name:str, db_path=DB_PATH) -> (bool, str):
    rechnungstellerDTO = read_rechnungssteller_by_name(db_path,rechnungsteller_name)
    if not rechnungstellerDTO:
        return None
    else:
        return rechnungstellerDTO.iban


if __name__ == '__main__':
    # print(ist_valide_iban("GB33BUKB20201555555555"))
    iban_aktualisieren("A", "GB33BUKB20201555555555")
