import os
from tkinter import messagebox
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import DateEntry

from datenbank.person import read_all_personen
from services.rechnung_services import *
from services.rechnungssteller_services import lade_alle_rechnungssteller


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

    rechnungssteller_dict = lade_alle_rechnungssteller()

    ttk.Label(frame, text="Rechnungssteller").grid(row=1, column=0, sticky=W, padx=5, pady=8)

    combo_rechnungssteller = ttk.Combobox(
        frame,
        values=list(rechnungssteller_dict.keys()),
        state="readonly",
        bootstyle="primary"
    )
    combo_rechnungssteller.grid(row=1, column=1, sticky=EW, padx=5, pady=8)

    ttk.Label(frame, text="IBAN").grid(row=2, column=0, sticky=W, padx=5, pady=8)

    iban_var = ttk.StringVar()
    entry_iban = ttk.Entry(frame, textvariable=iban_var, state="readonly")
    entry_iban.grid(row=2, column=1, sticky=EW, padx=5, pady=8)

    def on_rechnungssteller_select(event):
        name = combo_rechnungssteller.get()
        iban_var.set(rechnungssteller_dict[name])

    combo_rechnungssteller.bind("<<ComboboxSelected>>", on_rechnungssteller_select)

    ttk.Label(frame, text='Rechnungsdatum').grid(row=3, column=0, sticky=W, padx=5, pady=8)
    entry_datum = DateEntry(frame, bootstyle="primary", dateformat="%d.%m.%Y")
    entry_datum.grid(row=3, column=1, sticky=EW, padx=5, pady=8)

    ttk.Label(frame, text='Betrag in €').grid(row=4, column=0, sticky=W, padx=5, pady=8)
    entry_betrag = ttk.Entry(frame)
    entry_betrag.grid(row=4, column=1, sticky=EW, padx=5, pady=8)

    ttk.Label(frame, text='Verwendungszweck').grid(row=5, column=0, sticky=W, padx=5, pady=8)
    entry_verwendungszweck = ttk.Entry(frame)
    entry_verwendungszweck.grid(row=5, column=1, sticky=EW, padx=5, pady=8)

    def klick_rechnung_eingabe():
        person = combo_person.get()
        if not person:
            messagebox.showerror("Unvollständige Angaben","Keine Person ausgewählt")
            return
        person_id = personen_dict[person]

        rechnungssteller = combo_rechnungssteller.get()
        if not rechnungssteller:
            messagebox.showerror("Unvollständige Angaben","Kein Rechnungssteller ausgewählt")
            return

        betrag = entry_betrag.get()

        if not ist_gueltiger_betrag(betrag):
            messagebox.showerror("Fehler", "Betrag muss Format 123,45 oder 123.45 haben.")
            return

        verwendungszweck = entry_verwendungszweck.get()
        datum = entry_datum.entry.get()

        ist_eingefuegt, message = neue_rechnung_erfassen(
            person_id,
            rechnungssteller,
            datum,
            betrag,
            verwendungszweck)
        if ist_eingefuegt:
            messagebox.showinfo("Info", message)
            eingabe_button.configure(state="disabled")
        else:
            messagebox.showerror("Fehler beim Einfügen", message)

        if entry_iban.get() != "":
            image = erzeuge_epc_qr_code(rechnungssteller, betrag, verwendungszweck)
            img = ImageTk.PhotoImage(image)
            qr_code_label.configure(image=img)
            qr_code_label.image = img

    eingabe_button = ttk.Button(frame, text="Eingabe", bootstyle="success", command=klick_rechnung_eingabe)
    eingabe_button.grid(row=6, column=0, columnspan=2, sticky=EW, pady=20)


    qr_code_label = ttk.Label(frame)
    qr_code_label.grid(row=7, column=0, columnspan=2, pady=10)

    return frame

if __name__ == '__main__':
    app = ttk.Window("Neue Rechnung erfassen")
    app.geometry("800x600")
    frame = setup(app)
    frame.pack(fill=BOTH,expand=YES)
    app.mainloop()