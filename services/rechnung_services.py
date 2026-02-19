import re

from datenbank.person import read_person_by_id
from datenbank.rechnung import *
from datenbank.rechnung import RechnungDTO
from datenbank.rechnungssteller import read_rechnungssteller_by_name
from qr_codes.epc_qr_code import create_epc_qrcode
from datetime import datetime


def neue_rechnung_erfassen(person_id: int, rechnungssteller: str, rechnungsdatum: str, betrag: str, verwendungszweck: str):
    try:
        betrag = float(betrag.replace(",", "."))
    except ValueError:
        return False, "Ungültiger Betrag."

    rechnungsstellerDTO = read_rechnungssteller_by_name(rechnungssteller)
    if not rechnungsstellerDTO:
        return False, "Rechnungssteller existiert nicht."
    rechnungssteller_id = rechnungsstellerDTO.id
    rechnungsdatum_iso = datum_to_iso(rechnungsdatum)
    rechnungDTO = read_rechnung(person_id, rechnungssteller_id, rechnungsdatum_iso, betrag, verwendungszweck)
    if rechnungDTO:
        return False, "Rechnung existiert bereits."

    create_rechnung(person_id, rechnungssteller_id, rechnungsdatum_iso, betrag, verwendungszweck)
    return True, "Rechnung eingefügt."


def ist_gueltiger_betrag(betrag_str: str) -> bool:
    pattern = r"^\d+([.,]\d{1,2})?$"
    return re.fullmatch(pattern, betrag_str) is not None


def erzeuge_epc_qr_code(rechnungsteller: str, betrag: float, verwendungszweck: str):
    rechnungstellerDTO = read_rechnungssteller_by_name(rechnungsteller)
    return create_epc_qrcode(rechnungstellerDTO.name, rechnungstellerDTO.iban, betrag, verwendungszweck)


def alle_offenen_rechnungen_von_person(person_id: int):
    personDTO = read_person_by_id(person_id)
    if not personDTO:
        return None, "Person existiert nicht."
    rechnungen = read_offene_rechnungen_von_person_id(person_id)
    if not rechnungen:
        return None, "Keine offenen Rechnungen vorhanden."
    return rechnungen, "Rechnungen erfolgreich geladen."

def ist_gueltiges_datum(datum_str: str) -> bool:
    try:
        datetime.strptime(datum_str, "%d.%m.%Y")
        return True
    except ValueError:
        return False

def datum_to_iso(datum_str: str) -> str:
    return datetime.strptime(datum_str, "%d.%m.%Y").strftime("%Y-%m-%d")

def datum_iso_to_aneige(datum_iso: str) -> str:
    return datetime.strptime(datum_iso, "%Y-%m-%d").strftime("%d.%m.%Y")


def setze_abrechnungsdatum(rechnungen:list[RechnungDTO], abrechnungsdatum:str) -> (bool,str):
    if rechnungen is None:
        return False, "Keine Rechnungen ausgewählt."
    if not ist_gueltiges_datum(abrechnungsdatum):
        return False, "Abrechnungsdatum ungültig."
    for re in rechnungen:
        update_abrechnungsdatum(re.id, datum_to_iso(abrechnungsdatum))
    return True, "Abrechnungsdatum erfolgreich gesetzt."


if __name__ == '__main__':
    rechnungen, _ = alle_offenen_rechnungen_von_person(4)

    a, msg = setze_abrechnungsdatum(rechnungen, "29.01.2024")
    print(msg)