import requests

def create_epc_qrcode(empfaenger:str, iban:str, betrag:float, vwz:str):
    """
    Funktion zum Erstellen eines Überweisungscodes. Speicherung als PNG.
    Siehe: https://qrcode.tec-it.com/de/SEPA
    """
    url = f"https://qrcode.tec-it.com/API/QRCode?data=BCD%0a002%0a1%0aSCT%0a%0a{empfaenger}%0a{iban}%0aEUR{betrag}%0a%0a%0a{vwz}&errorcorrection=M&backcolor=%23ffffff"
    response = requests.get(url)
    if response.status_code == 200:
        with open("qr_code.png", "wb") as f:
            f.write(response.content)
        print("QR-Code gespeichert als qr_code.png")
    else:
        print("Fehler beim Abrufen:", response.status_code)

if __name__ == '__main__':
    create_epc_qrcode("Test","DE1235512423423",100,"123124ksdfe")