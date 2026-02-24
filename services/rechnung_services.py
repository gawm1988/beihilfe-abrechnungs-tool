import re
from datetime import datetime
from io import BytesIO

import requests
from PIL import Image

from datenbank.person import read_person_by_id
from datenbank.rechnung import *
from datenbank.rechnung import RechnungDTO
from datenbank.rechnungssteller import read_rechnungssteller_by_name
from services.dokumenten_services import *
from utils.paths import DB_PATH


def neue_rechnung_erfassen(person_id: int, rechnungssteller_id: int, rechnungsdatum: str, betrag: str,
                           verwendungszweck: str, db_path: str = DB_PATH):
    try:
        betrag = float(betrag.replace(",", "."))
    except ValueError:
        return False, "Ungültiger Betrag."
    rechnungsdatum_iso = datum_to_iso(rechnungsdatum)
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
    return create_epc_qrcode(rechnungstellerDTO.name, rechnungstellerDTO.iban, betrag, verwendungszweck)


def alle_offenen_rechnungen_von_person(person_id: int, db_path: str = DB_PATH):
    personDTO = read_person_by_id(db_path, person_id)
    if not personDTO:
        return None, "Person existiert nicht."
    rechnungen = read_offene_rechnungen_von_person_id(db_path, person_id)
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


def datum_iso_to_deutsches_format(datum_iso: str) -> str:
    return datetime.strptime(datum_iso, "%Y-%m-%d").strftime("%d.%m.%Y")


def setze_abrechnungsdatum(rechnungen: list[RechnungDTO], abrechnungsdatum: str, db_path: str = DB_PATH) -> (bool, str):
    if rechnungen is None:
        return False, "Keine Rechnungen ausgewählt."
    if not ist_gueltiges_datum(abrechnungsdatum):
        return False, "Abrechnungsdatum ungültig."
    for re in rechnungen:
        update_abrechnungsdatum(db_path, re.id, datum_to_iso(abrechnungsdatum))
    return True, "Abrechnungsdatum erfolgreich gesetzt."


def rechnung_pdf_speichern(rechnung_id: int, db_path: str = DB_PATH):
    hashwert = pdf_laden_und_speichern()
    if not hashwert:
        return False, "Upload nicht erfolgreich."
    update_pdf_path(db_path, rechnung_id, hashwert)
    return True, "Datei hochgeladen."


def rechnung_anzeigen(pdf_path: str):
    pdf_oeffnen_und_anzeigen(pdf_path)
