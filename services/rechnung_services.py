import re
from datetime import datetime
from io import BytesIO

import requests
from PIL import Image

from datenbank.person import read_person_by_id
from datenbank.rechnung import *
from datenbank.rechnungssteller import read_rechnungssteller_by_name
from utils.paths import DB_PATH


def neue_rechnung_erfassen(person_id: int, rechnungssteller_id: int, rechnungsdatum: str, betrag: str,
                           verwendungszweck: str, db_path: str = DB_PATH)->(bool,str):
    if ist_gueltiger_betrag(betrag):
        betrag = float(betrag.replace(",", "."))
    else:
        return False, "Ungültiger Betrag."
    rechnungsdatum_iso = datum_to_iso(rechnungsdatum)
    if not rechnungsdatum_iso:
        return False, "Ungültiges Datumsformat."
    rechnungDTO = read_rechnung(db_path,person_id, rechnungssteller_id, rechnungsdatum_iso, betrag, verwendungszweck)
    if rechnungDTO:
        return False, "Rechnung existiert bereits."

    create_rechnung(db_path, person_id,rechnungssteller_id, rechnungsdatum_iso, betrag, verwendungszweck)
    return True, "Rechnung eingefügt."


def neue_rechnung_erfassen_mit_rechnungssteller_namen(person_id: int, rechnungssteller: str, rechnungsdatum: str,
                                                      betrag: str,
                                                      verwendungszweck: str, db_path: str = DB_PATH):
    rechnungsstellerDTO = read_rechnungssteller_by_name(db_path, rechnungssteller)
    if not rechnungsstellerDTO:
        return False, "Rechnungssteller existiert nicht."
    return neue_rechnung_erfassen(person_id, rechnungsstellerDTO.id, rechnungsdatum, betrag,
                           verwendungszweck, db_path)


def ist_gueltiger_betrag(betrag_str: str) -> bool:
    pattern = r"^\d+([.,]\d{1,2})?$"
    return re.fullmatch(pattern, betrag_str) is not None


def create_epc_qrcode(empfaenger: str, iban: str, betrag: float, vwz: str) -> Image:
    # https://qrcode.tec-it.com/de/SEPA
    url = f"https://qrcode.tec-it.com/API/QRCode?data=BCD%0a002%0a1%0aSCT%0a%0a{empfaenger}%0a{iban}%0aEUR{betrag}%0a%0a%0a{vwz}&errorcorrection=M&backcolor=%23ffffff"
    response = requests.get(url)
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content)).resize((200, 200))
        return image
    else:
        print("Fehler beim Abrufen:", response.status_code)
        return None


def erzeuge_epc_qr_code(rechnungsteller: str, betrag: float, verwendungszweck: str, db_path: str = DB_PATH):
    rechnungstellerDTO = read_rechnungssteller_by_name(db_path, rechnungsteller)
    if not rechnungstellerDTO:
        return None
    elif rechnungstellerDTO.iban == "":
        return None
    print(rechnungstellerDTO.iban)
    return create_epc_qrcode(rechnungstellerDTO.name, rechnungstellerDTO.iban, betrag, verwendungszweck)


def alle_offenen_rechnungen_von_person(person_id: int, db_path: str = DB_PATH):
    personDTO = read_person_by_id(db_path, person_id)
    if not personDTO:
        return None, "Person existiert nicht."
    rechnungen = read_offene_rechnungen_von_person_id(db_path, person_id)
    if not rechnungen:
        return None, "Keine offenen Rechnungen vorhanden."
    return rechnungen, "Rechnungen erfolgreich geladen."

def datum_to_iso(datum_str: str) -> str | None:
    for fmt in ("%Y-%m-%d", "%d.%m.%Y"):
        try:
            dt = datetime.strptime(datum_str, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None

def datum_to_deutsches_format(datum_str: str) -> str | None:
    for fmt in ("%Y-%m-%d", "%d.%m.%Y"):
        try:
            dt = datetime.strptime(datum_str, fmt)
            return dt.strftime("%d.%m.%Y")
        except ValueError:
            continue
    return None

def rechnung_hashwert_speichern(rechnung_id: int, hashwert:str, db_path: str = DB_PATH):
    if not hashwert:
        return False, "Upload nicht erfolgreich."
    ist_vorhanden = read_rechnung_by_hashwert(db_path, hashwert)
    if ist_vorhanden:
       return False, "Rechnung doppelt hinterlegt."
    update_hashwert(db_path, rechnung_id, hashwert)
    return True, "Datei hochgeladen."

def lade_rechnung_by_person_rechnungssteller_datum(person_id:int,rechnungssteller_id:int, rechnungsdatum:str, db_path: str = DB_PATH):
    datum = datum_to_iso(rechnungsdatum)
    rechnungDTO = read_rechnung_by_id_person_rechnungssteller(db_path,person_id,rechnungssteller_id,datum)
    if not rechnungDTO:
        return None
    return rechnungDTO

def setze_abrechnung_id(person_id:int, abrechnung_id:int, db_path: str = DB_PATH):
    rechnungen = read_rechnungen_by_abrechnung_id(db_path, abrechnung_id)
    if rechnungen:
        return False, "Abrechnung_ID existiert bereits."
    rechnungen , message = alle_offenen_rechnungen_von_person(person_id, db_path)
    if not rechnungen:
        return False , message
    update_abrechnung_id(db_path, person_id, abrechnung_id)
    return True, f"Abrechnung_ID {abrechnung_id} erfolgreich gesetzt."
