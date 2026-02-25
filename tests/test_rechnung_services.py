import json
import tempfile
import os
from unittest import TestCase


from datenbank.connection import create_tabellen
from services.person_services import neue_person_erfassen, lade_person_by_name
from services.rechnung_services import *
from services.rechnungssteller_services import neuen_rechnungsteller_erfassen, lade_rechnungssteller_by_name
from utils.paths import TEST_RESOURCES_DIR


class Rechnung_Test(TestCase):

    def setUp(self):
        self.db_path = os.path.join(
            tempfile.gettempdir(),
            f"{self._testMethodName}.db"
        )
        print(self.db_path)
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except PermissionError:
                import time
                time.sleep(0.1)
                os.remove(self.db_path)
        create_tabellen(self.db_path)

    def testrechnungen_anlegen(self):
        with open(TEST_RESOURCES_DIR, "r", encoding="utf-8") as f:
            data = json.load(f)
        for p in data["personen"]:
            neue_person_erfassen(p["vorname"], p["nachname"], p["beihilfesatz"], self.db_path)
        for r in data["rechnungssteller"]:
            neuen_rechnungsteller_erfassen(r["name"], r["iban"], self.db_path)
        for re in data["rechnungen"]:
            neue_rechnung_erfassen(re["person_id"], re["rechnungssteller_id"], re["rechnungsdatum"], re["betrag"],
                                   re["verwendungszweck"], self.db_path)

    def test_neue_rechnung_erfassen(self):
        neue_person_erfassen("Theodor", "Testperson", "0.85", self.db_path)
        personDTO = lade_person_by_name("Theodor", "Testperson", self.db_path)
        neuen_rechnungsteller_erfassen("Testfirma", "", self.db_path)
        rechnungsstellerDTO = lade_rechnungssteller_by_name("Testfirma", self.db_path)
        # Betrag ungültig
        ist_eingefuegt, _ = neue_rechnung_erfassen(personDTO.id, rechnungsstellerDTO.id, "31.01.2020", "a",
                                                   "Test-Rechnung", self.db_path)
        self.assertFalse(ist_eingefuegt)
        # Datum ungültig
        ist_eingefuegt, _ = neue_rechnung_erfassen(personDTO.id, rechnungsstellerDTO.id, "01/31/2020", "123,45",
                                                   "Test-Rechnung", self.db_path)
        self.assertFalse(ist_eingefuegt)

        ist_eingefuegt, _ = neue_rechnung_erfassen(personDTO.id, rechnungsstellerDTO.id, "31.01.2020", "123,45",
                                                   "Test-Rechnung", self.db_path)
        self.assertTrue(ist_eingefuegt)
        # Bereits eingefügt
        ist_eingefuegt, _ = neue_rechnung_erfassen(personDTO.id, rechnungsstellerDTO.id, "31.01.2020", "123,45",
                                                   "Test-Rechnung", self.db_path)
        self.assertFalse(ist_eingefuegt)

    def test_ist_gueltiger_betrag(self):
        self.assertTrue(ist_gueltiger_betrag("1"))
        self.assertTrue(ist_gueltiger_betrag("0"))
        self.assertTrue(ist_gueltiger_betrag("1,2"))
        self.assertTrue(ist_gueltiger_betrag("1.2"))
        self.assertTrue(ist_gueltiger_betrag("1,23"))
        self.assertTrue(ist_gueltiger_betrag("1.23"))
        self.assertFalse(ist_gueltiger_betrag("1,234"))
        self.assertFalse(ist_gueltiger_betrag("1.234"))
        self.assertFalse(ist_gueltiger_betrag("1,234,567"))
        self.assertFalse(ist_gueltiger_betrag("1.234.567"))
        self.assertFalse(ist_gueltiger_betrag("1.234,567"))
        self.assertFalse(ist_gueltiger_betrag("1,234.567"))
        self.assertFalse(ist_gueltiger_betrag("a"))
        self.assertFalse(ist_gueltiger_betrag(" "))

    def test_neue_rechnung_erfassen_mit_rechnungssteller_namen(self):
        neue_person_erfassen("Theodor", "Testperson", "0.85", self.db_path)
        personDTO = lade_person_by_name("Theodor", "Testperson", self.db_path)
        neuen_rechnungsteller_erfassen("Testfirma", "", self.db_path)
        rechnungsstellerDTO = lade_rechnungssteller_by_name("Testfirma", self.db_path)
        # Betrag ungültig
        ist_eingefuegt, _ = neue_rechnung_erfassen(personDTO.id, rechnungsstellerDTO.name, "31.01.2020", "a",
                                                   "Test-Rechnung", self.db_path)
        self.assertFalse(ist_eingefuegt)
        # Datum ungültig
        ist_eingefuegt, _ = neue_rechnung_erfassen(personDTO.id, rechnungsstellerDTO.name, "01/31/2020", "123,45",
                                                   "Test-Rechnung", self.db_path)
        self.assertFalse(ist_eingefuegt)

        ist_eingefuegt, _ = neue_rechnung_erfassen(personDTO.id, rechnungsstellerDTO.name, "31.01.2020", "123,45",
                                                   "Test-Rechnung", self.db_path)
        self.assertTrue(ist_eingefuegt)
        # Bereits eingefügt
        ist_eingefuegt, _ = neue_rechnung_erfassen(personDTO.id, rechnungsstellerDTO.name, "31.01.2020", "123,45",
                                                   "Test-Rechnung", self.db_path)
        self.assertFalse(ist_eingefuegt)

    def test_create_epc_qrcode(self):
        img = create_epc_qrcode("Testfirma","GB33BUKB20201555555555",12.34,"Testrechnung")
        self.assertTrue(isinstance(img,Image.Image))

    def test_erzeuge_epc_qr_code(self):
        neuen_rechnungsteller_erfassen("Testfirma", "", self.db_path)
        rechnugnsstellerDTO = lade_rechnungssteller_by_name("Testfirma", self.db_path)
        img = erzeuge_epc_qr_code(rechnugnsstellerDTO.name,12.34,"Testrechnung",self.db_path)
        self.assertEqual(img,None)
        neuen_rechnungsteller_erfassen("Testfirma1", "GB33BUKB20201555555555", self.db_path)
        rechnugnsstellerDTO = lade_rechnungssteller_by_name("Testfirma1", self.db_path)
        img = erzeuge_epc_qr_code(rechnugnsstellerDTO.name, 12.34, "Testrechnung", self.db_path)
        self.assertTrue(isinstance(img, Image.Image))

    def test_alle_offenen_rechnungen_von_person(self):
        # Person existiert nicht
        rechnungen, _ = alle_offenen_rechnungen_von_person(1, self.db_path)
        self.assertEqual(None, rechnungen)

        neue_person_erfassen("Theodor", "Testperson", "0.85", self.db_path)
        personDTO = lade_person_by_name("Theodor", "Testperson", self.db_path)
        neuen_rechnungsteller_erfassen("Testfirma", "", self.db_path)
        rechnungsstellerDTO = lade_rechnungssteller_by_name("Testfirma", self.db_path)

        # Keine Rechnung zu Person
        rechnungen, _ = alle_offenen_rechnungen_von_person(personDTO.id, self.db_path)
        self.assertEqual(None, rechnungen)

        neue_rechnung_erfassen(personDTO.id, rechnungsstellerDTO.id, "31.01.2020", "123,45",
                               "Test-Rechnung", self.db_path)
        neue_rechnung_erfassen(personDTO.id, rechnungsstellerDTO.id, "31.01.2021", "123,45",
                               "Test-Rechnung", self.db_path)

        neue_rechnung_erfassen(personDTO.id, rechnungsstellerDTO.id, "31.01.2022", "123,45",
                               "Test-Rechnung", self.db_path)
        rechnungen, _ = alle_offenen_rechnungen_von_person(personDTO.id, self.db_path)
        self.assertEqual(3, len(rechnungen))


    def test_datum_to_iso(self):
        datum_iso = "2020-01-31"
        datum_dt = "31.01.2020"
        self.assertEqual(datum_iso, datum_to_iso(datum_dt))
        self.assertEqual(datum_iso, datum_to_iso(datum_iso))
        self.assertEqual(None, datum_to_iso("01/31/2020"))
        self.assertEqual(None, datum_to_iso("a"))


    def test_datum_to_deutsches_format(self):
        datum_iso = "2020-01-31"
        datum_dt = "31.01.2020"
        self.assertEqual(datum_dt, datum_to_deutsches_format(datum_dt))
        self.assertEqual(datum_dt, datum_to_deutsches_format(datum_iso))
        self.assertEqual(None, datum_to_deutsches_format("01/31/2020"))
        self.assertEqual(None, datum_to_deutsches_format("a"))

    def test_rechnungspfad_speichern(self):
        neue_person_erfassen("Theodor", "Testperson", "0.85", self.db_path)
        personDTO = lade_person_by_name("Theodor", "Testperson", self.db_path)
        neuen_rechnungsteller_erfassen("Testfirma", "", self.db_path)
        rechnungsstellerDTO = lade_rechnungssteller_by_name("Testfirma", self.db_path)
        rechnungsdatum = "31.01.2020"
        neue_rechnung_erfassen(personDTO.id, rechnungsstellerDTO.id, rechnungsdatum, "12,34",
                                                   "Test-Rechnung", self.db_path)
        rechnungDTO = lade_rechnung_by_person_rechnungssteller_datum(personDTO.id, rechnungsstellerDTO.id, rechnungsdatum,self.db_path)
        hashwert = "0123456789abcdef"
        rechnungspfad_speichern(rechnungDTO.id,hashwert,self.db_path)
        rechnungDTO = lade_rechnung_by_person_rechnungssteller_datum(personDTO.id, rechnungsstellerDTO.id,
                                                                     rechnungsdatum, self.db_path)
        self.assertEqual(rechnungDTO.pdf_path,hashwert)

    def test_lade_rechnung_by_person_rechnungssteller_datum(self):
        neue_person_erfassen("Theodor", "Testperson", "0.85", self.db_path)
        personDTO = lade_person_by_name("Theodor", "Testperson", self.db_path)
        neuen_rechnungsteller_erfassen("Testfirma", "", self.db_path)
        rechnungsstellerDTO = lade_rechnungssteller_by_name("Testfirma", self.db_path)
        rechnungsdatum = "31.01.2020"
        neue_rechnung_erfassen(personDTO.id, rechnungsstellerDTO.id, rechnungsdatum, "12,34",
                               "Test-Rechnung", self.db_path)
        rechnungDTO = lade_rechnung_by_person_rechnungssteller_datum(personDTO.id, rechnungsstellerDTO.id,
                                                                     rechnungsdatum, self.db_path)
        self.assertEqual(rechnungDTO.person_id,personDTO.id)
        self.assertEqual(rechnungDTO.rechnungssteller_id, rechnungsstellerDTO.id)
        self.assertEqual(rechnungDTO.rechnungsdatum, datum_to_iso(rechnungsdatum))
        rechnungDTO = lade_rechnung_by_person_rechnungssteller_datum(personDTO.id, rechnungsstellerDTO.id,
                                                                     "01.12.1999", self.db_path)
        self.assertEqual(None, rechnungDTO)