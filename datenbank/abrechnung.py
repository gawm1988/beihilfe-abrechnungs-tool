from datenbank.connection import connect


class AbrechnungDTO:
    id: int
    abrechnungsdatum: str
    gesamtbetrag: float
    beihilfebetrag: float
    pkv_betrag: float
    hashwert: str

    def __init__(self, id: int, abrechnungsdatum: str, gesamtbetrag: float, beihilfebetrag: float, pkv_betrag: float,
                 hashwert: str):
        self.id = id
        self.abrechnungsdatum = abrechnungsdatum
        self.gesamtbetrag = gesamtbetrag
        self.beihilfebetrag = beihilfebetrag
        self.pkv_betrag = pkv_betrag
        self.hashwert = hashwert


def create_abrechnung(db_path: str, abrechnungsdatum: str, gesamtbetrag: float):
    with(connect(db_path)) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO abrechnung (abrechnungsdatum, gesamtbetrag) VALUES (?, ?)",
            (abrechnungsdatum, gesamtbetrag)
        )


def read_abrechnung_by_id(db_path: str, abrechnung_id: str):
    with(connect(db_path)) as conn:
        cursor = conn.cursor()
        fetch = cursor.execute(
            "SELECT * FROM abrechnung WHERE id = ? ",
            (abrechnung_id,)
        ).fetchone()
        if not fetch:
            return None
        return AbrechnungDTO(*fetch)


def update_abrechnung_beihilfebetrag(db_path: str, abrechnung_id: str, beihilfebetrag: float):
    with(connect(db_path)) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE abrechnung SET beihilfebetrag = ? WHERE id = ?",
            (beihilfebetrag, abrechnung_id)
        )


def update_abrechnung_pkv_betrag(db_path: str, abrechnung_id: str, pkv_betrag: float):
    with(connect(db_path)) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE abrechnung SET pkv_betrag = ? WHERE id = ?",
            (pkv_betrag, abrechnung_id)
        )


def update_abrechnung_hashwert(db_path: str, abrechnung_id: str, hashwert: str):
    with(connect(db_path)) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE abrechnung SET hashwert = ? WHERE id = ?",
            (hashwert, abrechnung_id)
        )
