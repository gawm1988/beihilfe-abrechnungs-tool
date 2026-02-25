import json
import os
import tempfile
from unittest import TestCase

from datenbank.connection import create_tabellen
from services.person_services import ist_gueltiger_beihilfesatz, neue_person_erfassen, lade_alle_personen_dict, \
    lade_person_by_name
from utils.paths import TEST_RESOURCES_DIR


class Personen_Test(TestCase):

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

    def testpersonen_anlegen(self):
        with open(TEST_RESOURCES_DIR, "r", encoding="utf-8") as f:
            data = json.load(f)
        for p in data["personen"]:
            neue_person_erfassen(p["vorname"], p["nachname"], p["beihilfesatz"], self.db_path)

    def test_neue_person_erfassen(self):
        vorname = "Thea"
        nachname = "Testperson"
        beihilfesatz = "0,8"
        # neue Person anlegen
        ist_eingefuegt, _ = neue_person_erfassen(vorname, nachname, beihilfesatz, self.db_path)
        self.assertTrue(ist_eingefuegt)
        # neue Person schon vorhanden
        ist_eingefuegt, _ = neue_person_erfassen(vorname, nachname, beihilfesatz, self.db_path)
        self.assertFalse(ist_eingefuegt)
        leer = ""
        ist_eingefuegt, _ = neue_person_erfassen(leer, nachname, self.db_path)
        self.assertFalse(ist_eingefuegt)
        ist_eingefuegt, _ = neue_person_erfassen(vorname, leer, self.db_path)
        self.assertFalse(ist_eingefuegt)

    def test_ist_gueltiger_beihilfesatz(self):
        # gültige Formate
        self.assertTrue(ist_gueltiger_beihilfesatz("0,1"))
        self.assertTrue(ist_gueltiger_beihilfesatz("0,12"))
        self.assertTrue(ist_gueltiger_beihilfesatz("0.1"))
        self.assertTrue(ist_gueltiger_beihilfesatz("0.12"))
        # ungültige Formate
        self.assertFalse(ist_gueltiger_beihilfesatz("0,123"))
        self.assertFalse(ist_gueltiger_beihilfesatz("0.123"))
        self.assertFalse(ist_gueltiger_beihilfesatz("0"))
        self.assertFalse(ist_gueltiger_beihilfesatz("1"))
        self.assertFalse(ist_gueltiger_beihilfesatz("1,2"))
        self.assertFalse(ist_gueltiger_beihilfesatz("1.2"))
        self.assertFalse(ist_gueltiger_beihilfesatz("a"))

    def test_lade_alle_personen_dict(self):
        self.assertEqual(None, lade_alle_personen_dict(self.db_path))
        self.testpersonen_anlegen()
        personen_dict = lade_alle_personen_dict(self.db_path)
        self.assertEqual(4, len(personen_dict))

    def test_lade_person_by_name(self):
        vorname = "Tristan"
        nachname = "Testperson"
        self.assertEqual(None,lade_person_by_name(vorname,nachname,self.db_path))
        neue_person_erfassen(vorname,nachname,"0,8",self.db_path)
        personDTO = lade_person_by_name(vorname,nachname,self.db_path)
        self.assertEqual(vorname,personDTO.vorname)
        self.assertEqual(nachname,personDTO.nachname)