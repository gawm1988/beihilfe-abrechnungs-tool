import os

from datenbank.connection import create_tabellen

TEST_DB = "test.db"

personen = [
    ["Anton","Anlagenbauer","0,8"],
    ["Berta","Bildhauerin","0,75"],
    ["Christian","Chemikermeister","0,55"],
    ["Dora","Dachdeckerin","0.35"]
]

def test_setup():
    if os.path.isfile("test.db"):
        os.remove(TEST_DB)
        print("Alte DB gelöscht.")
    create_tabellen("test.db")
    print("Neue DB angelegt.")

if __name__ == '__main__':
    test_setup()