import re
from datenbank.rechnung import create_rechnung, read_rechnung
from datenbank.rechnungssteller import read_rechnungssteller_by_id
from qr_codes.epc_qr_code import create_epc_qrcode

def neue_rechnung_erfassen(person_id:int,rechnungssteller_id:int,datum:str,betrag:str,vwz:str)->bool:
    betrag = float(betrag.replace(",", "."))
    exist = read_rechnung(person_id,rechnungssteller_id,datum,betrag,vwz)
    if exist:
        print(f"Rechnung existiert bereits: {person_id} → {rechnungssteller_id}: {betrag} - {vwz} vom {datum}.")
        return False
    else:
        create_rechnung(person_id,rechnungssteller_id,datum,betrag,vwz)
        print(f"Rechnung eingefügt: {person_id} → {rechnungssteller_id}: {betrag} €, {vwz} vom {datum}.")
        return True

def ist_gueltiger_betrag(betrag_str: str) -> bool:
    pattern = r"^\d+([.,]\d{1,2})?$"
    return re.fullmatch(pattern, betrag_str) is not None

def erzeuge_epc_qr_code(rechnungsteller_id:int, betrag:float, verwendungszweck:str):
    rechnungstellerDTO = read_rechnungssteller_by_id(rechnungsteller_id)
    return create_epc_qrcode(rechnungstellerDTO.name,rechnungstellerDTO.iban,betrag,verwendungszweck)


