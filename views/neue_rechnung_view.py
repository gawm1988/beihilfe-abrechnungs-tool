import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import DateEntry

from datenbank.sql_queries import neue_rechnung_erfassen

def setup(master):
    frame = ttk.Frame(master, padding=20)

    frame.columnconfigure(1, weight=1)

    # Vorname
    ttk.Label(frame, text='Vorname').grid(row=0, column=0, sticky=W, padx=5, pady=8)
    entry_vorname = ttk.Entry(frame)
    entry_vorname.grid(row=0, column=1, sticky=EW, padx=5, pady=8)

    # Nachname
    ttk.Label(frame, text='Nachname').grid(row=1, column=0, sticky=W, padx=5, pady=8)
    entry_nachname = ttk.Entry(frame)
    entry_nachname.grid(row=1, column=1, sticky=EW, padx=5, pady=8)

    # Leistungsbringer
    ttk.Label(frame, text='Rechnungssteller').grid(row=2, column=0, sticky=W, padx=5, pady=8)
    entry_leistungsbringer = ttk.Entry(frame)
    entry_leistungsbringer.grid(row=2, column=1, sticky=EW, padx=5, pady=8)

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
        neue_rechnung_erfassen(
            entry_vorname.get(),
            entry_nachname.get(),
            entry_leistungsbringer.get(),
            entry_datum.entry.get(),
            entry_betrag.get(),
            entry_vwz.get())

    ttk.Button(frame, text='Eingabe', bootstyle="success", command=klick_rechnung_eingabe)\
        .grid(row=6, column=0, columnspan=2, sticky=EW, pady=20)

    return frame

if __name__ == '__main__':
    app = ttk.Window("Neue Rechnung erfassen")
    app.geometry("800x600")
    frame = setup(app)
    frame.pack(fill=BOTH,expand=YES)
    app.mainloop()