import os
import json
import tempfile
from unittest import TestCase

from datenbank.connection import create_tabellen

from services.rechnungssteller_services import *


class Rechnungssteller_Test(TestCase):
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

    def testrechnungssteller_anlegen(self):
        with open("tests/ressources/testdaten.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        for r in data["rechnungssteller"]:
            neuen_rechnungsteller_erfassen(r["name"], r["iban"], self.db_path)

    def test_neuen_rechnungsteller_erfassen(self):
        name = "Test Rechnungssteller"
        iban = "DE02300606010002474689"
        ist_eingefuegt, _ = neuen_rechnungsteller_erfassen(name, iban, self.db_path)
        self.assertTrue(ist_eingefuegt)
        ist_eingefuegt, _ = neuen_rechnungsteller_erfassen(name, iban, self.db_path)
        self.assertFalse(ist_eingefuegt)

    def test_lade_alle_rechnungssteller_iban_dict(self):
        self.assertEqual(None, lade_alle_rechnungssteller_iban_dict(self.db_path))
        name = "Test Rechnungssteller"
        iban = "DE02300606010002474689"
        neuen_rechnungsteller_erfassen(name, iban, self.db_path)
        self.testrechnungssteller_anlegen()
        rechnungsteller_dict = lade_alle_rechnungssteller_iban_dict(self.db_path)
        last_key, last_value = next(reversed(rechnungsteller_dict.items()))
        self.assertEqual(5, len(rechnungsteller_dict))
        self.assertEqual(last_key, name)
        self.assertEqual(last_value, iban)

    def test_lade_alle_rechnungssteller_dict(self):
        self.assertEqual(None, lade_alle_rechnungssteller_dict(self.db_path))
        name = "Test Rechnungssteller"
        iban = "DE02300606010002474689"
        neuen_rechnungsteller_erfassen(name, iban, self.db_path)
        self.testrechnungssteller_anlegen()
        rechnungsteller_dict = lade_alle_rechnungssteller_dict(self.db_path)
        self.assertEqual(5, len(rechnungsteller_dict))
        test_value = rechnungsteller_dict.get(1)  # erster Tabelleneintrag
        self.assertEqual(test_value, name)

    def test_iban_aktualisieren(self):
        name = "Test Rechnungssteller"
        iban = ""
        neuen_rechnungsteller_erfassen(name, iban, self.db_path)
        test_iban = "DE02300606010002474689"
        neuen_rechnungsteller_erfassen(name, iban, self.db_path)
        self.assertNotEqual(test_iban, lade_iban(name, self.db_path))
        iban_aktualisieren(name, test_iban, self.db_path)
        self.assertEqual(test_iban, lade_iban(name, self.db_path))

    def test_lade_iban(self):
        name = "Test Rechnungssteller"
        iban = "DE02300606010002474689"
        neuen_rechnungsteller_erfassen(name, iban, self.db_path)
        self.assertEqual(iban, lade_iban(name, self.db_path))

    def test_ist_valide_iban(self):
        self.assertTrue(ist_valide_iban(""))
        self.assertTrue(ist_valide_iban("DE02300606010002474689"))
        # nur gültige IBAN werden akzeptiert
        # https://ibanvalidieren.de/beispiele.html
        self.assertFalse(ist_valide_iban(" "))
        self.assertFalse(ist_valide_iban(None))
        self.assertFalse(ist_valide_iban(2))
        self.assertFalse(ist_valide_iban("DE12345678901234567890"))
        self.assertFalse(ist_valide_iban("00DE123456789012345678"))
