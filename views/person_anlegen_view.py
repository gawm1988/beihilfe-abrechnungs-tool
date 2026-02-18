from tkinter import messagebox

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from services.person_services import neue_person_erfassen, ist_gueltiger_beihilfesatz


def setup(master)->ttk.Frame:
    frame = ttk.Frame(master, padding=20)
    frame.columnconfigure(1, weight=1)

    ttk.Label(frame, text="Vorname").grid(row=0, column=0, sticky=W, padx=5, pady=8)
    entry_vorname = ttk.Entry(frame, width=20)
    entry_vorname.grid(row=0, column=1, sticky=EW, padx=5, pady=8)

    ttk.Label(frame,text="Nachname").grid(row=1, column=0, sticky=W, padx=5, pady=8)
    entry_nachname = ttk.Entry(frame, width=20)
    entry_nachname.grid(row=1, column=1, sticky=EW, padx=5, pady=8)

    ttk.Label(frame, text="Beihilfesatz").grid(row=2, column=0, sticky=W, padx=5, pady=8)
    entry_beihilfesatz = ttk.Entry(frame, width=20)
    entry_beihilfesatz.grid(row=2, column=1, sticky=EW, padx=5, pady=8)

    def klick_person_anlegen():
        vorname = entry_vorname.get()
        nachname = entry_nachname.get()
        beihilfesatz = entry_beihilfesatz.get()

        ist_eingefuegt, message = neue_person_erfassen(vorname, nachname, beihilfesatz)
        if ist_eingefuegt:
            messagebox.showinfo("✅ Erfolgreich eingefügt",message)
            person_anlegen_button.configure(state=DISABLED)
        else:
            messagebox.showerror("Fehler", message)


    person_anlegen_button = ttk.Button(frame,text="Eingabe", bootstyle="success", command=klick_person_anlegen)
    person_anlegen_button.grid(row=3, column=0, columnspan=2, sticky=EW, pady=20)

    return frame

if __name__ == '__main__':
    app = ttk.Window()
    app.geometry("800x600")
    frame = setup(app)
    frame.pack()
    app.mainloop()