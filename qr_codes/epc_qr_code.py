import requests
from io import BytesIO
from PIL import Image

def create_epc_qrcode(empfaenger:str, iban:str, betrag:float, vwz:str)->Image:
    # https://qrcode.tec-it.com/de/SEPA
    url = f"https://qrcode.tec-it.com/API/QRCode?data=BCD%0a002%0a1%0aSCT%0a%0a{empfaenger}%0a{iban}%0aEUR{betrag}%0a%0a%0a{vwz}&errorcorrection=M&backcolor=%23ffffff"
    response = requests.get(url)
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content)).resize((200,200))
        return image
    else:
        print("Fehler beim Abrufen:", response.status_code)
        return None