import tkinter as tk
from functools import partial
from tkinter import messagebox
from tkinter.messagebox import showerror

import ttkbootstrap as ttk
from PIL import ImageTk
from ttkbootstrap import DateEntry
from ttkbootstrap.constants import *

from services.abrechung_services import erstelle_abrechnung
from services.rechnung_services import *
from services.person_services import lade_alle_personen_dict
from services.rechnungssteller_services import lade_alle_rechnungssteller_dict, lade_iban
from services.dokumenten_services import pdf_laden_und_speichern, pdf_oeffnen_und_anzeigen


def setup(master) -> ttk.Frame:
    frame = ttk.Frame(master, padding=20)
    frame.columnconfigure(0, weight=0)
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(4, weight=1)

    personen_dict = lade_alle_personen_dict()

    ttk.Label(frame, text="Person").grid(row=0, column=0, sticky=W, padx=5, pady=8)

    combo_person = ttk.Combobox(
        frame,
        values=list(personen_dict.keys()),
        state="readonly",
        bootstyle="primary"
    )
    combo_person.grid(row=0, column=1, sticky=EW, padx=5, pady=5)

    ttk.Label(frame, text="Offene Rechnungen").grid(
        row=3, column=0, columnspan=2, sticky=W, padx=5, pady=8
    )

    scroll_container = ttk.Frame(frame)
    scroll_container.grid(row=4, column=0, columnspan=2, sticky="nsew")

    scroll_container.rowconfigure(0, weight=1)
    scroll_container.columnconfigure(0, weight=1)

    canvas = tk.Canvas(scroll_container, highlightthickness=0)
    canvas.grid(row=0, column=0, sticky="nsew")

    scrollbar = ttk.Scrollbar(
        scroll_container,
        orient="vertical",
        command=canvas.yview
    )
    scrollbar.grid(row=0, column=1, sticky="ns")

    canvas.configure(yscrollcommand=scrollbar.set)

    rechnungen_frame = ttk.Frame(canvas)
    rechnungen_frame.columnconfigure(0, weight=1)
    rechnungen_frame.columnconfigure(1, weight=1)

    canvas_window = canvas.create_window(
        (0, 0),
        window=rechnungen_frame,
        anchor="nw"
    )

    def update_scrollregion(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    rechnungen_frame.bind("<Configure>", update_scrollregion)

    def resize_frame(event):
        canvas.itemconfigure(canvas_window, width=event.width)

    canvas.bind("<Configure>", resize_frame)

    def on_person_select(event):
        person = combo_person.get()
        person_id = personen_dict.get(person)

        for widget in rechnungen_frame.winfo_children():
            widget.destroy()

        rechnungssteller_dict = lade_alle_rechnungssteller_dict()

        rechnungen, message = alle_offenen_rechnungen_von_person(person_id)
        if rechnungen is None:
            messagebox.showerror("Fehler", message)
            return

        for index, r in enumerate(rechnungen):
            rechnungssteller_name = rechnungssteller_dict.get(r.rechnungssteller_id)
            rechnungsdatum = datum_to_deutsches_format(r.rechnungsdatum)
            betrag = r.betrag
            verwendungszweck = r.verwendungszweck

            row = index // 2
            col = index % 2

            rechnungen_frame.rowconfigure(row, weight=1)

            card = ttk.Labelframe(
                rechnungen_frame,
                text=rechnungssteller_name,
                padding=10,
                bootstyle="info"
            )
            card.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)

            text = (
                f"Betrag: {betrag} €\n"
                f"Verwendungszweck: {verwendungszweck}\n"
                f"Datum: {rechnungsdatum}"
            )

            label = ttk.Label(card, text=text, justify=LEFT)
            label.pack(anchor="w", fill=BOTH, expand=YES)

            button_frame = ttk.Frame(card)
            button_frame.pack(anchor="e", pady=5)

            def upload_pdf(rechnung_id):
                hashwert = pdf_laden_und_speichern()
                rechnung_hashwert_speichern(rechnung_id, hashwert)
                on_person_select(None)

            def lade_qr_code(rechnungsteller_name, betrag, verwendungszweck):
                image = erzeuge_epc_qr_code(rechnungssteller_name, betrag, verwendungszweck)
                img = ImageTk.PhotoImage(image)
                qr_code_label.configure(image=img)
                qr_code_label.image = img

            if lade_iban(rechnungssteller_name):
                ttk.Button(
                    button_frame,
                    text="🔳",
                    width=3,
                    bootstyle="info-outline",
                    command=partial(lade_qr_code, rechnungssteller_name, betrag, verwendungszweck)
                ).pack(side="left", padx=3)

            if r.hashwert:
                ttk.Button(
                    button_frame,
                    text="👁",
                    width=3,
                    bootstyle="secondary-outline",
                    command=lambda p=r.hashwert: pdf_oeffnen_und_anzeigen(p)
                ).pack(side="left", padx=3)

            else:
                ttk.Button(
                    button_frame,
                    text="📎",
                    width=3,
                    bootstyle="secondary-outline",
                    command=partial(upload_pdf, r.id)
                ).pack(side="left", padx=3)

            def update_wraplength(event):
                label.config(wraplength=event.width)

            label.bind("<Configure>", update_wraplength)

    combo_person.bind("<<ComboboxSelected>>", on_person_select)

    qr_code_label = ttk.Label(frame)
    qr_code_label.grid(row=5, column=0, columnspan=2, pady=10)

    entry_datum = DateEntry(frame, bootstyle="primary", dateformat="%d.%m.%Y")
    entry_datum.grid(row=6, column=0, sticky=W, padx=5, pady=8)

    def klick_abrechnung():
        person = combo_person.get()
        person_id = personen_dict.get(person)
        abrechnungsdatum = entry_datum.entry.get()
        ist_abgerechnet, message = erstelle_abrechnung(person_id,abrechnungsdatum)
        if not ist_abgerechnet:
            messagebox.showerror("Fehler", message)
            return
        messagebox.showinfo("✅ Erfolgreich abgerechnet", message)
        on_person_select(None)


    abrechnung_button = ttk.Button(frame, text="Abrechnung erstellen", command=klick_abrechnung)
    abrechnung_button.grid(row=6, column=1,  sticky=EW,  pady=10)

    return frame


if __name__ == "__main__":
    app = ttk.Window()
    app.geometry("800x600")
    frame = setup(app)
    frame.pack(fill=BOTH, expand=YES)
    app.mainloop()
