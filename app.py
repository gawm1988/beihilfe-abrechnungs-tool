import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import views.neue_rechnung_view
import views.rechnungssteller_anlegen_view
import views.rechnungssteller_aktualisieren_view

class App(ttk.Window):
    FONT = ("Segoe UI", 18)

    def __init__(self):
        super().__init__(themename="darkly")
        self.title("Beihilfe Abrechnung")
        self.geometry("1000x800")

        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_content_area()

    # ----------------------------
    # Sidebar
    # ----------------------------
    def create_sidebar(self):
        self.sidebar = ttk.Frame(self, padding=10, bootstyle="secondary")
        self.sidebar.grid(row=0, column=0, sticky="ns")

        ttk.Button(
            self.sidebar,
            text="Neue Rechnung",
            bootstyle="light",
            command=self.show_neue_rechnung
        ).pack(fill=X, pady=5)

        ttk.Button(
            self.sidebar,
            text="Rechnungssteller",
            bootstyle="light",
            command=self.show_rechnungssteller_erfassen
        ).pack(fill=X, pady=5)

        ttk.Button(
            self.sidebar,
            text="IBAN",
            bootstyle="light",
            command=self.show_rechnungssteller_aktualisieren
        ).pack(fill=X, pady=5)

        ttk.Button(
            self.sidebar,
            text="Personen",
            bootstyle="light",
            command=self.show_personen
        ).pack(fill=X, pady=5)

        ttk.Button(
            self.sidebar,
            text="Übersicht",
            bootstyle="light",
            command=self.show_uebersicht
        ).pack(fill=X, pady=5)

    # ----------------------------
    # Content Bereich
    # ----------------------------
    def create_content_area(self):
        self.content = ttk.Frame(self, padding=20)
        self.content.grid(row=0, column=1, sticky="nsew")

    # ----------------------------
    # Frame-Wechsel-Logik
    # ----------------------------
    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_neue_rechnung(self):
        self.clear_content()
        ttk.Label(self.content, text="Neue Rechnung erfassen", font=self.FONT).pack()
        frame = views.neue_rechnung_view.setup(self.content)
        frame.pack(fill=X)

    def show_personen(self):
        self.clear_content()
        ttk.Label(self.content, text="Personenverwaltung", font=self.FONT).pack()

    def show_uebersicht(self):
        self.clear_content()
        ttk.Label(self.content, text="Übersicht", font=self.FONT).pack()

    def show_rechnungssteller_erfassen(self):
        self.clear_content()
        ttk.Label(self.content, text="Neuen Rechnungssteller erfassen", font=self.FONT).pack()
        frame = views.rechnungssteller_anlegen_view.setup(self.content)
        frame.pack(fill=X)

    def show_rechnungssteller_aktualisieren(self):
        self.clear_content()
        ttk.Label(self.content, text="IBAN aktualisieren", font=self.FONT).pack()
        frame = views.rechnungssteller_aktualisieren_view.setup(self.content)
        frame.pack(fill=X)



if __name__ == "__main__":
    app = App()
    app.mainloop()
