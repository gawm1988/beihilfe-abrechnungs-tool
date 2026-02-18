from tkinter import messagebox

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from services.rechnungssteller_services import lade_alle_rechnungssteller, iban_aktualisieren


def setup(master)->ttk.Frame:
    frame = ttk.Frame(master, padding=20)
    frame.columnconfigure(1, weight=1)

    rechnungssteller_dict = lade_alle_rechnungssteller()

    ttk.Label(frame, text="Rechnungssteller").grid(row=0, column=0, sticky=W, padx=5, pady=8)

    combo_rechnungssteller = ttk.Combobox(
        frame,
        values=list(rechnungssteller_dict.keys()),
        state="readonly",
        bootstyle="primary"
    )
    combo_rechnungssteller.grid(row=0, column=1, sticky=EW, padx=5, pady=8)

    ttk.Label(frame, text="IBAN").grid(row=1, column=0, sticky=W, padx=5, pady=8)

    iban_var = ttk.StringVar()
    entry_iban = ttk.Entry(frame, textvariable=iban_var)
    entry_iban.grid(row=1, column=1, sticky=EW, padx=5, pady=8)

    def on_rechnungssteller_select(event):
        name = combo_rechnungssteller.get()
        iban_var.set(rechnungssteller_dict[name])

    combo_rechnungssteller.bind("<<ComboboxSelected>>", on_rechnungssteller_select)

    def klick_iban_aktualisieren():
        rechnungsteller_name = combo_rechnungssteller.get()
        rechnungsteller_iban = entry_iban.get()
        ist_aktualisiert_iban, message = iban_aktualisieren(rechnungsteller_name, rechnungsteller_iban)
        if ist_aktualisiert_iban:
            messagebox.showinfo("✅ IBAN erfolgreich aktualisiert",message)
            iban_aktualisieren_button.configure(state=DISABLED)
        else:
            messagebox.showerror("Fehler", message)


    iban_aktualisieren_button = ttk.Button(frame,text="Eingabe", bootstyle="success", command=klick_iban_aktualisieren)
    iban_aktualisieren_button.grid(row=2, column=0, columnspan=2, sticky=EW, pady=20)

    return frame

if __name__ == '__main__':
    app = ttk.Window("Neue Rechnung erfassen")
    app.geometry("800x600")
    frame = setup(app)
    frame.pack(fill=BOTH,expand=YES)
    app.mainloop()