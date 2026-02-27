from datenbank.abrechnung import *
from datenbank.testdaten import testdaten_anlegen
from services.dokumenten_services import pdf_dateien_zusammenfuehren
from services.rechnung_services import alle_offenen_rechnungen_von_person, setze_abrechnung_id, ist_gueltiger_betrag
from utils.paths import DB_PATH

def erstelle_abrechnung(person_id:int, abrechnungsdatum:str, db_path: str = DB_PATH)->(bool, str):
    rechnungen, msg = alle_offenen_rechnungen_von_person(person_id, db_path)
    if not rechnungen:
        return False, msg
    gesamtbetrag = 0.0
    pdf_liste = []
    for re in rechnungen:
        gesamtbetrag += re.betrag
        if not re.hashwert:
            return False, "Nicht alle Dokumente hochgeladen."
        pdf_liste.append(f"{re.hashwert}.pdf")
    abrechnungDTO = create_abrechnung(db_path,person_id,abrechnungsdatum, gesamtbetrag)
    ist_gesetzt, msg = setze_abrechnung_id(person_id, abrechnungDTO.id)
    if not ist_gesetzt:
        delete_abrechung(db_path, abrechnungDTO.id)
        return False, msg

    hashwert = pdf_dateien_zusammenfuehren(pdf_liste)
    update_abrechnung_hashwert(db_path,abrechnungDTO.id, hashwert)
    return "Neue Abrechnung angelegt"

def setze_beihilfebetrag(abrechnung_id:int, beihilfebetrag:str, db_path: str = DB_PATH)->(bool, str):
    abrechnungDTO = read_abrechnung_by_id(db_path, abrechnung_id)
    if not abrechnungDTO:
        return False, "Abrechnung nicht vorhanden."
    if not ist_gueltiger_betrag(beihilfebetrag):
        return False, "Betrag ungültig."
    update_abrechnung_beihilfebetrag(db_path, abrechnungDTO.id, float(beihilfebetrag))
    return True, "Beihilfeerstattung ergänzt."

def setze_pkv_betrag(abrechnung_id:int, pkv_betrag:str, db_path: str = DB_PATH)->(bool, str):
    abrechnungDTO = read_abrechnung_by_id(db_path, abrechnung_id)
    if not abrechnungDTO:
        return False, "Abrechnung nicht vorhanden."
    if not ist_gueltiger_betrag(pkv_betrag):
        return False, "Betrag ungültig."
    update_abrechnung_pkv_betrag(db_path, abrechnungDTO.id, float(pkv_betrag))
    return True, "PKV-Erstattung ergänzt."

if __name__ == '__main__':
    testdaten_anlegen()
    print(erstelle_abrechnung(1,"2025-12-31"))
    print(setze_pkv_betrag(1,"100"))
    print(setze_beihilfebetrag(1,"100.1"))


