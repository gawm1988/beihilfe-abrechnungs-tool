from tkinter import messagebox
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from datenbank.person import read_all_personen
from services.rechnung_services import *
from services.rechnungssteller_services import lade_alle_rechnungssteller


def setup(master) -> ttk.Frame:
    frame = ttk.Frame(master, padding=20)
    frame.columnconfigure(0, weight=0)
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(4, weight=1)

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

        rechnungssteller_dict = lade_alle_rechnungssteller()

        rechnungen, message = alle_offenen_rechnungen_von_person(person_id)
        if rechnungen is None:
            messagebox.showerror("Fehler", message)
            return

        for index, r in enumerate(rechnungen):
            rechnungssteller_name = rechnungssteller_dict.get(r.rechnungssteller_id)
            rechnungsdatum = datum_iso_to_aneige(r.rechnungsdatum)
            betrag = r.betrag
            verwendungszweck = r.verwendungszweck

            row = index // 2
            col = index % 2

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

            def update_wraplength(event):
                label.config(wraplength=event.width)

            label.bind("<Configure>", update_wraplength)

    combo_person.bind("<<ComboboxSelected>>", on_person_select)

    return frame

if __name__ == "__main__":
    app = ttk.Window()
    app.geometry("800x600")
    frame = setup(app)
    frame.pack(fill=BOTH, expand=YES)
    app.mainloop()
