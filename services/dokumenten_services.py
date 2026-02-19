from tkinter import filedialog
import hashlib
from pathlib import Path
import shutil
import os
import platform
import subprocess

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

if __name__ == '__main__':
    pdf_auswaehlen()
