import collections

from schwifty import IBAN

from datenbank.rechnungssteller import *


def ist_valide_iban(iban: str):
    if iban == "":
        return True
    try:
        iban = IBAN(iban)
        return True
    except ValueError:
        return False


def neuen_rechnungsteller_erfassen(name: str, iban: str) -> (bool, str):
    rechnungstellerDTO = read_rechnungssteller_by_name(name)
    if rechnungstellerDTO:
        return False, "Rechnungssteller existiert bereits."

    if not ist_valide_iban(iban):
        return False, f"IBAN {iban} ist ungültig."

    create_rechnungssteller(name, iban)
    return True, f"Rechnungssteller {name} angelegt.\nIBAN: {iban}"


def lade_alle_rechnungssteller_iban() -> dict[str, str]:
    rechnungssteller = read_alle_rechnungssteller_mit_iban()
    rechnungssteller_dict = {
        name: iban
        for name, iban in rechnungssteller
    }
    return collections.OrderedDict(sorted(rechnungssteller_dict.items()))


def lade_alle_rechnungssteller() -> dict[int, str]:
    rechnungssteller = read_alle_rechnungssteller()
    return {
        rid: name
        for rid, name in rechnungssteller
    }


def iban_aktualisieren(name: str, iban: str) -> (bool, str):
    if not ist_valide_iban(iban):
        return False, f"IBAN {iban} ist ungültig."

    rechnungstellerDTO = read_rechnungssteller_by_name(name)
    if not rechnungstellerDTO:
        return False, f"Rechnungssteller {name} existiert nicht."

    update_iban(name, iban)
    return True, f"Rechnungssteller {name} aktualisiert.\nIBAN: {iban}"


if __name__ == '__main__':
    # print(ist_valide_iban("GB33BUKB20201555555555"))
    iban_aktualisieren("A", "GB33BUKB20201555555555")
