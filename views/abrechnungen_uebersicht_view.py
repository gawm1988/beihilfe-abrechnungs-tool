import tkinter as tk
from functools import partial
from tkinter import messagebox

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from services.abrechung_services import lade_alle_abrechnungen_von_person_id, setze_beihilfebetrag, setze_pkv_betrag
from services.dokumenten_services import pdf_oeffnen_und_anzeigen
from services.person_services import lade_alle_personen_dict


def speichern_erstattung(
    abrechnung_id,
    beihilfe_var,
    pkv_var,
    entry_beihilfe,
    entry_pkv
):
    beihilfe = beihilfe_var.get().strip()
    pkv = pkv_var.get().strip()

    try:
        if beihilfe:
            setze_beihilfebetrag(abrechnung_id, beihilfe)
            entry_beihilfe.configure(state="readonly")

        if pkv:
            setze_pkv_betrag(abrechnung_id, pkv)
            entry_pkv.configure(state="readonly")

    except Exception as e:
        messagebox.showerror("Fehler", str(e))
        return

    messagebox.showinfo("Erfolg", "Erstattungsbetrag gespeichert.")


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

    ttk.Label(frame, text="Abrechnungen").grid(
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

    abrechnungen_frame = ttk.Frame(canvas)
    abrechnungen_frame.columnconfigure(0, weight=1)
    abrechnungen_frame.columnconfigure(1, weight=1)

    canvas_window = canvas.create_window(
        (0, 0),
        window=abrechnungen_frame,
        anchor="nw"
    )

    def update_scrollregion(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    abrechnungen_frame.bind("<Configure>", update_scrollregion)

    def resize_frame(event):
        canvas.itemconfigure(canvas_window, width=event.width)

    canvas.bind("<Configure>", resize_frame)

    def on_person_select(event):
        person = combo_person.get()
        person_id = personen_dict.get(person)

        for widget in abrechnungen_frame.winfo_children():
            widget.destroy()

        abrechnungen, message = lade_alle_abrechnungen_von_person_id(person_id)

        if abrechnungen is None:
            messagebox.showerror("Fehler", message)
            return

        ttk.Label(abrechnungen_frame, text="Datum", width=15).grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(abrechnungen_frame, text="Gesamt", width=12).grid(row=0, column=1, padx=5)
        ttk.Label(abrechnungen_frame, text="Beihilfe", width=12).grid(row=0, column=2, padx=5)
        ttk.Label(abrechnungen_frame, text="PKV", width=12).grid(row=0, column=3, padx=5)
        ttk.Label(abrechnungen_frame, text="Speichern").grid(row=0, column=4)
        ttk.Label(abrechnungen_frame, text="PDF").grid(row=0, column=5)

        for index, a in enumerate(abrechnungen, start=1):

            # Datum
            ttk.Label(
                abrechnungen_frame,
                text=a.abrechnungsdatum
            ).grid(row=index, column=0, padx=5, pady=5)

            # Gesamtbetrag
            ttk.Label(
                abrechnungen_frame,
                text=f"{a.gesamtbetrag:.2f} €"
            ).grid(row=index, column=1, padx=5)

            # Beihilfe Entry
            beihilfe_var = tk.StringVar(
                value="" if a.beihilfebetrag is None else str(a.beihilfebetrag)
            )

            entry_beihilfe = ttk.Entry(
                abrechnungen_frame,
                textvariable=beihilfe_var,
                width=12
            )

            if a.beihilfebetrag is not None:
                entry_beihilfe.configure(state="readonly")

            entry_beihilfe.grid(row=index, column=2, padx=5)

            # PKV Entry
            pkv_var = tk.StringVar(
                value="" if a.pkv_betrag is None else str(a.pkv_betrag)
            )

            entry_pkv = ttk.Entry(
                abrechnungen_frame,
                textvariable=pkv_var,
                width=12
            )

            if a.pkv_betrag is not None:
                entry_pkv.configure(state="readonly")

            entry_pkv.grid(row=index, column=3, padx=5)

            btn_speichern = ttk.Button(
                abrechnungen_frame,
                text="Speichern",
                bootstyle="success",
                command=partial(
                    speichern_erstattung,
                    a.id,
                    beihilfe_var,
                    pkv_var,
                    entry_beihilfe,
                    entry_pkv
                )
            )
            btn_speichern.grid(row=index, column=4, padx=5)

            # PDF Button
            btn_pdf = ttk.Button(
                abrechnungen_frame,
                text="PDF öffnen",
                bootstyle="info-outline",
                command=partial(pdf_oeffnen_und_anzeigen, a.hashwert)
            )
            if a.pkv_betrag is not None and a.beihilfebetrag is not None:
                btn_speichern.configure(state="disabled")

            btn_pdf.grid(row=index, column=5, padx=5)

    combo_person.bind("<<ComboboxSelected>>", on_person_select)

    return frame


if __name__ == "__main__":
    app = ttk.Window()
    app.geometry("800x600")
    frame = setup(app)
    frame.pack(fill=BOTH, expand=YES)
    app.mainloop()
