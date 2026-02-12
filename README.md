# Beihilfe- und Krankenkassenabrechnung
## Beschreibung
Anwendung zur Unterstützung bei der Abrechnung von ausgelegten Rechnungen sowohl bei der Krankenkasse als auch bei der Beihilfestellung.
## Anforderungen
- [ ] Rechnungen einscannen und Rechnungsdetails automatisch erkennen
- [ ] Bereitstellung von Überweisungs-QR-Codes
- [ ] Übersicht der offenen Posten: 
  - Einzelübersicht der Rechnungen, Empfänger, Re-Nr., Zahlungsdatum, Summe, hinterlegte PDF
  - Gesamtsumme aller offenen Posten, davon Anteil Krankenkasse bzw. Beihilfe
  - Mehrere Personen: Versicherungsnehmer + mitversicherte / beihilfeberechtigte Personen
- [ ] Automatische Abrechnung auf Knopfdruck:
  - Bereitstellung der PDF-Dateien für Krankenkassenupload
  - Versanddeckblatt für Versand Beihilfe Dokumente
- [ ] Historie vergangener Abrechnungen
  - Erstattung durch Leistungsträger
  - Übersicht der Leistungskürzungen, mit Begründung
  - Vorlage für Widerspruch zu bestimmten Positionen
- [ ] Benutzerfreundliches Dashboard.
## Technische Umsetzung
- [ ] Programmiersprache Python (oder JAVA)
- [ ] Library zum Auslesen der Rechnungsdaten (z.B. [invoice2data](https://github.com/invoice-x/invoice2data))
- [ ] Datenbank zur Speicherung der Rechnungsdaten 
- [ ] API Einbindung für Generierung der Überweisungscodes
