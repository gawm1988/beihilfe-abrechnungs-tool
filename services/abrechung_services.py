from datenbank.abrechnung import *
from services.dokumenten_services import pdf_dateien_zusammenfuehren
from services.rechnung_services import alle_offenen_rechnungen_von_person, setze_abrechnung_id
from utils.paths import DB_PATH

def erstelle_abrechnung(person_id:int, abrechnungsdatum:str, db_path: str = DB_PATH):
    rechnungen, msg = alle_offenen_rechnungen_von_person(person_id, db_path)
    if not rechnungen:
        return msg
    gesamtbetrag = 0.0
    pdf_liste = []
    for re in rechnungen:
        gesamtbetrag += re.betrag
        if not re.hashwert:
            return "Fehler: Nicht alle Dokumente hochgeladen."
        pdf_liste.append(f"{re.hashwert}.pdf")
    abrechnungDTO = create_abrechnung(db_path,abrechnungsdatum, gesamtbetrag)
    ist_gesetzt, msg = setze_abrechnung_id(person_id, abrechnungDTO.id)
    if not ist_gesetzt:
        return msg

    hashwert = pdf_dateien_zusammenfuehren(pdf_liste)
    update_abrechnung_hashwert(db_path,abrechnungDTO.id, hashwert)


if __name__ == '__main__':
    print(erstelle_abrechnung(1,"2025-12-31"))

