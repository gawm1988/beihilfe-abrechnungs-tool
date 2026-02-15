import re
import os
from tkinter import messagebox
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import DateEntry

from datenbank.sqlite_database import create_rechnung, read_all_personen, read_all_rechnungssteller

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QR_PATH = os.path.join(BASE_DIR, "qr_codes", "qr_code.png")

def ist_gueltiger_betrag(betrag_str: str) -> bool:
    pattern = r"^\d+([.,]\d{1,2})?$"
    return re.fullmatch(pattern, betrag_str) is not None

def setup(master)->ttk.Frame:
    frame = ttk.Frame(master, padding=20)

    frame.columnconfigure(1, weight=1)

    personen = read_all_personen()
    personen_dict = {
        f"{vorname} {nachname}": pid
        for pid, vorname, nachname in personen
    }

    ttk.Label(frame, text="Person").grid(row=0, column=0, sticky=W, padx=5, pady=8)

    combo_person = ttk.Combobox(
        frame,
        values=list(personen_dict.keys()),
        state="readonly",
        bootstyle="primary"
    )
    combo_person.grid(row=0, column=1, sticky=EW, padx=5, pady=8)

    rechnungssteller = read_all_rechnungssteller()
    rechnungssteller_dict = {
        f"{name}": lid
        for lid, name in rechnungssteller
    }

    ttk.Label(frame, text="Rechnungssteller").grid(row=1, column=0, sticky=W, padx=5, pady=8)

    combo_rechnungssteller = ttk.Combobox(
        frame,
        values=list(rechnungssteller_dict.keys()),
        state="readonly",
        bootstyle="primary"
    )
    combo_rechnungssteller.grid(row=1, column=1, sticky=EW, padx=5, pady=8)

    # Datum
    ttk.Label(frame, text='Rechnungsdatum').grid(row=3, column=0, sticky=W, padx=5, pady=8)
    entry_datum = DateEntry(frame, bootstyle="primary", dateformat="%d.%m.%Y")
    entry_datum.grid(row=3, column=1, sticky=EW, padx=5, pady=8)

    # Betrag
    ttk.Label(frame, text='Betrag in €').grid(row=4, column=0, sticky=W, padx=5, pady=8)
    entry_betrag = ttk.Entry(frame)
    entry_betrag.grid(row=4, column=1, sticky=EW, padx=5, pady=8)

    # Verwendungszweck
    ttk.Label(frame, text='Verwendungszweck').grid(row=5, column=0, sticky=W, padx=5, pady=8)
    entry_vwz = ttk.Entry(frame)
    entry_vwz.grid(row=5, column=1, sticky=EW, padx=5, pady=8)

    def klick_rechnung_eingabe():
        person = combo_person.get()
        if not person:
            print("Keine Person ausgewählt")
            return
        person_id = personen_dict[person]

        rechnungssteller = combo_rechnungssteller.get()
        if not rechnungssteller:
            print("Kein Rechnungssteller ausgewählt")
            return
        rechnungssteller_id = rechnungssteller_dict[rechnungssteller]

        betrag = entry_betrag.get()

        if not ist_gueltiger_betrag(betrag):
            messagebox.showerror("Fehler", "Betrag muss Format 123,45 oder 123.45 haben.")
            return

        vwz = entry_vwz.get()
        datum = entry_datum.entry.get()

        ist_eingefuegt = create_rechnung(
            person_id,
            rechnungssteller_id,
            datum,
            betrag,
            vwz)
        if ist_eingefuegt:
            title = f"{person} -> {rechnungssteller}: € {betrag}, Vwz: {vwz} vom {datum}."
            messagebox.showinfo(title, "Rechnung erfolgreich eingefügt.")
            title_var.set(title)

            image = Image.open(QR_PATH).resize((200, 200))
            img = ImageTk.PhotoImage(image)
            qr_code_label.configure(image=img)
            qr_code_label.image = img

            eingabe_button.configure(state="disabled")

        else:
            messagebox.showinfo("Info", "Rechnung nicht eingefügt.")

    eingabe_button = ttk.Button(frame, text='Eingabe', bootstyle="success", command=klick_rechnung_eingabe)
    eingabe_button.grid(row=6, column=0, columnspan=2, sticky=EW, pady=20)

    title_var = ttk.StringVar()
    qr_code_label = ttk.Label(frame, textvariable=title_var)
    qr_code_label.grid(row=7, column=0, columnspan=2, pady=10)

    qr_code_label = ttk.Label(frame)
    qr_code_label.grid(row=8, column=0, columnspan=2, pady=10)



    return frame

if __name__ == '__main__':
    app = ttk.Window("Neue Rechnung erfassen")
    app.geometry("800x600")
    frame = setup(app)
    frame.pack(fill=BOTH,expand=YES)
    app.mainloop()