from pathlib import Path
import sys

# Spezialfall für PyInstaller
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "datenbank"
PDF_DIR = BASE_DIR / "rechnungen"
DB_PATH = DATA_DIR / "beihilfe.db"

# Ordner automatisch anlegen
PDF_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)
