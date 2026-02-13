from datenbank.sqlite_database import create_rechnung


def neue_rechnung_erfassen(person_vorname:str, person_nachname:str, leistungsbringer:str,datum:str,betrag:float,verwendungszweck:str):
    try:
        betrag = betrag.replace(",", ".")
    except ValueError:
        print("Ungültiger Betrag")
        return
    create_rechnung(person_vorname,person_nachname,leistungsbringer,datum,betrag,verwendungszweck)
