import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import DateEntry

from datenbank.sqlite_database import create_rechnung, read_all_personen, read_all_leistungsbringer

def setup(master):
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

    leistungsbringer = read_all_leistungsbringer()
    leistungsbringer_dict = {
        f"{name}": lid
        for lid, name in leistungsbringer
    }

    ttk.Label(frame, text="Rechnungssteller").grid(row=1, column=0, sticky=W, padx=5, pady=8)

    combo_leistungsbringer = ttk.Combobox(
        frame,
        values=list(leistungsbringer_dict.keys()),
        state="readonly",
        bootstyle="primary"
    )
    combo_leistungsbringer.grid(row=1, column=1, sticky=EW, padx=5, pady=8)

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

        leistungsbringer = combo_leistungsbringer.get()
        if not leistungsbringer:
            print("Kein Rechnungssteller ausgewählt")
            return
        leistungsbringer_id = leistungsbringer_dict[leistungsbringer]



        create_rechnung(
            person_id,
            leistungsbringer_id,
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