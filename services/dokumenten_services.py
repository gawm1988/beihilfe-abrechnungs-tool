import hashlib
import os
import platform
import shutil
import subprocess
from tkinter import filedialog

from pypdf import PdfWriter, PdfReader

from utils.paths import BASE_DIR, PDF_DIR


def berechne_hash(dateipfad):
    sha256 = hashlib.sha256()

    with open(dateipfad, "rb") as f:
        for block in iter(lambda: f.read(4096), b""):
            sha256.update(block)

    return sha256.hexdigest()

def pdf_laden_und_speichern():
    dateipfad = filedialog.askopenfilename(
        title="PDF auswählen",
        filetypes=[("PDF Dateien", "*.pdf")],
        initialdir=BASE_DIR
    )

    if not dateipfad:
        return None
    hashwert = berechne_hash(dateipfad)
    zielpfad = PDF_DIR / f"{hashwert}.pdf"

    if not zielpfad.exists():
        shutil.copy2(dateipfad, zielpfad)
    return hashwert

def pdf_oeffnen_und_anzeigen(hashwert:str):
    pdf_path = PDF_DIR / f"{hashwert}.pdf"
    if platform.system() == "Windows":
        os.startfile(pdf_path)
    elif platform.system() == "Darwin":
        subprocess.run(["open", pdf_path])
    else:
        subprocess.run(["xdg-open", pdf_path])


def pdf_dateien_zusammenfuehren(pdf_liste:list[str], rechnung_path = PDF_DIR)->str:
    writer = PdfWriter()

    for pdf in pdf_liste:
        reader = PdfReader(pdf)
        for page in reader.pages:
            writer.add_page(page)

    with open(f"{rechnung_path}/tmp.pdf", "wb") as f:
        writer.write(f)

    hashwert = berechne_hash(f"{rechnung_path}/tmp.pdf")
    if not os.path.isfile(f"{rechnung_path}/{hashwert}.pdf"):
        os.rename(f"{rechnung_path}/tmp.pdf", f"{rechnung_path}/{hashwert}.pdf")
    return hashwert

if __name__ == '__main__':

    pdfs = [BASE_DIR/"tests/resources/Testrechnung_Apotheke.pdf",BASE_DIR/"tests/resources/Testrechnung_Optiker.pdf",BASE_DIR/"tests/resources/Testrechnung_Physio.pdf"]
    print(pdf_dateien_zusammenfuehren(pdfs))

