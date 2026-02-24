import os
import json
import tempfile
from unittest import TestCase

from datenbank.connection import create_tabellen
from services.rechnungssteller_services import neuen_rechnungsteller_erfassen, lade_alle_rechnungssteller_iban_dict, lade_alle_rechnungssteller_dict


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
        self.assertEqual(None,lade_alle_rechnungssteller_iban_dict(self.db_path))
        name = "Test Rechnungssteller"
        iban = "DE02300606010002474689"
        neuen_rechnungsteller_erfassen(name, iban, self.db_path)
        self.testrechnungssteller_anlegen()
        rechnungsteller_dict = lade_alle_rechnungssteller_iban_dict(self.db_path)
        last_key, last_value = next(reversed(rechnungsteller_dict.items()))
        self.assertEqual(5, len(rechnungsteller_dict))
        self.assertEqual(last_key,name)
        self.assertEqual(last_value,iban)



    def test_lade_alle_rechnungssteller_dict(self):
        self.assertEqual(None, lade_alle_rechnungssteller_dict(self.db_path))
        self.testrechnungssteller_anlegen()
        rechnungsteller_dict = lade_alle_rechnungssteller_dict(self.db_path)
        self.assertEqual(4, len(rechnungsteller_dict))

    def test_iban_aktualisieren(self):
        self.fail()

    def test_lade_iban(self):
        self.fail()
