from unittest import TestCase

from services.person_services import ist_gueltiger_beihilfesatz, neue_person_erfassen
from tests.test_setup import test_setup
from utils.paths import DB_PATH

DB_PATH = "test.db"

class Test(TestCase):
    def test_neue_person_erfassen(self):
        test_setup()
        vorname = "Thea"
        nachname = "Testperson"
        beihilfesatz = "0,8"
        # neue Person anlegen
        eingefuegt, _ = neue_person_erfassen(vorname, nachname, beihilfesatz,DB_PATH)
        self.assertEqual(True, eingefuegt)
        # neue Person schon vorhanden
        eingefuegt, _ = neue_person_erfassen(vorname, nachname, beihilfesatz,DB_PATH)
        self.assertEqual(False, eingefuegt)


    def test_ist_gueltiger_beihilfesatz(self):
        # gültige Formate
        self.assertEqual(True, ist_gueltiger_beihilfesatz("0,1"))
        self.assertEqual(True, ist_gueltiger_beihilfesatz("0,12"))
        self.assertEqual(True, ist_gueltiger_beihilfesatz("0.1"))
        self.assertEqual(True, ist_gueltiger_beihilfesatz("0.12"))
        # ungültige Formate
        self.assertEqual(False, ist_gueltiger_beihilfesatz("0,123"))
        self.assertEqual(False, ist_gueltiger_beihilfesatz("0.123"))
        self.assertEqual(False, ist_gueltiger_beihilfesatz("0"))
        self.assertEqual(False, ist_gueltiger_beihilfesatz("1"))
        self.assertEqual(False, ist_gueltiger_beihilfesatz("1,2"))
        self.assertEqual(False, ist_gueltiger_beihilfesatz("1.2"))
        self.assertEqual(False, ist_gueltiger_beihilfesatz("a"))