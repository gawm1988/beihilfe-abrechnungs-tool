from tkinter import messagebox

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from services.rechnungssteller_services import neuen_rechnungsteller_erfassen


def setup(master)->ttk.Frame:
    frame = ttk.Frame(master, padding=20)
    frame.columnconfigure(1, weight=1)

    ttk.Label(frame, text="Rechnungssteller").grid(row=0, column=0, sticky=W, padx=5, pady=8)
    entry_rechnungssteller = ttk.Entry(frame, width=20)
    entry_rechnungssteller.grid(row=0, column=1, sticky=EW, padx=5, pady=8)

    ttk.Label(frame,text="IBAN").grid(row=1, column=0, sticky=W, padx=5, pady=8)
    entry_iban = ttk.Entry(frame, width=20)
    entry_iban.grid(row=1, column=1, sticky=EW, padx=5, pady=8)

    def klick_rechnungssteller_anlegen():
        rechnungsteller_name = entry_rechnungssteller.get()
        rechnungsteller_iban = entry_iban.get()
        ist_eingefuegt = neuen_rechnungsteller_erfassen(rechnungsteller_name, rechnungsteller_iban)
        if ist_eingefuegt:
            messagebox.showinfo("✅ Erfolgreich eingefügt",f"Rechnungssteller: {rechnungsteller_name}\nIBAN: {rechnungsteller_iban}.")
            rechnungsteller_anlegen_button.configure(state=DISABLED)
        else:
            messagebox.showerror("❌ Fehler", f"Rechnungsteller {rechnungsteller_name} existiert bereits.")


    rechnungsteller_anlegen_button = ttk.Button(frame,text="Eingabe", bootstyle="success", command=klick_rechnungssteller_anlegen)
    rechnungsteller_anlegen_button.grid(row=2, column=0, columnspan=2, sticky=EW, pady=20)

    return frame