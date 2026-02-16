import re
from datenbank.rechnung import create_rechnung, read_rechnung

def neue_rechnung_erfassen(person_id:int,rechnungssteller_id:int,datum:str,betrag:str,vwz:str)->bool:
    betrag = float(betrag.replace(",", "."))
    exist = read_rechnung(person_id,rechnungssteller_id,datum,betrag,vwz)
    if exist:
        print(f"Rechnung existiert bereits: {person_id} → {rechnungssteller_id}: {betrag} - {vwz} vom {datum}.")
        return False
    else:
        create_rechnung(person_id,rechnungssteller_id,datum,betrag,vwz)
        return True

def ist_gueltiger_betrag(betrag_str: str) -> bool:
    pattern = r"^\d+([.,]\d{1,2})?$"
    return re.fullmatch(pattern, betrag_str) is not None
