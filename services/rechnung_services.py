import re
from datenbank.rechnung import create_rechnung, read_rechnung, read_offene_rechnungen_von_person_id
from datenbank.rechnungssteller import read_rechnungssteller_by_id, read_rechnungssteller_by_name
from datenbank.person import read_person_by_id
from qr_codes.epc_qr_code import create_epc_qrcode

def neue_rechnung_erfassen(person_id: int,rechnungssteller: str,datum: str,betrag: str,verwendungszweck: str):
    try:
        betrag = float(betrag.replace(",", "."))
    except ValueError:
        return False, "Ungültiger Betrag."

    rechnungsstellerDTO = read_rechnungssteller_by_name(rechnungssteller)
    if not rechnungsstellerDTO:
        return False, "Rechnungssteller existiert nicht."
    rechnungssteller_id = rechnungsstellerDTO.id

    rechnungDTO = read_rechnung(person_id,rechnungssteller_id,datum,betrag,verwendungszweck)
    if rechnungDTO:
        return False, "Rechnung existiert bereits."

    create_rechnung(person_id,rechnungssteller_id,datum,betrag,verwendungszweck)
    return True, "Rechnung eingefügt."


def ist_gueltiger_betrag(betrag_str: str) -> bool:
    pattern = r"^\d+([.,]\d{1,2})?$"
    return re.fullmatch(pattern, betrag_str) is not None

def erzeuge_epc_qr_code(rechnungsteller:str, betrag:float, verwendungszweck:str):
    rechnungstellerDTO = read_rechnungssteller_by_name(rechnungsteller)
    return create_epc_qrcode(rechnungstellerDTO.name,rechnungstellerDTO.iban,betrag,verwendungszweck)

def alle_offenen_rechnungen_von_person(person_id: int):
    personDTO = read_person_by_id(person_id)
    if not personDTO:
        return None, "Person existiert nicht."
    rechnungen = read_offene_rechnungen_von_person_id(person_id)
    if not rechnungen:
        return None, "Keine offenen Rechnungen vorhanden."
    return rechnungen, "Rechnungen erfolgreich geladen."

if __name__ == '__main__':
    rechnungen,_ = alle_offenen_rechnungen_von_person(1)
    for r in rechnungen:
        print(r)