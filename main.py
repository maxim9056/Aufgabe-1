import tkinter as tk
from tkinter import ttk
import mariadb
import sys

# Klasse für Artikel
class Artikel:
    def __init__(self, artikelname, lagerbestand, lieferantenname):
        self.artikelname = artikelname
        self.lagerbestand = lagerbestand
        self.lieferantenname = lieferantenname

# Verbindung zur Datenbank
try:
    conn = mariadb.connect(
        user="horstMueller",
        password="Pommes1",
        host="localhost",
        port=3306,
        database="schlumpfshop3"
    )
except mariadb.Error as e:
    print("Fehler bei der Verbindung zur Datenbank:", e)
    sys.exit()

cur = conn.cursor()

#Abfrage
def artikel_abfragen():
    eingabe = eingabe_feld.get() # Holt den Text (also die Eingabe) aus dem Eingabefeld

    try:
        mindestmenge = int(eingabe)

       

        # Alte Tabelle löschen
        for eintrag in tabelle.get_children():  #löscht alle zeilen die in einer tabelle stehen
            tabelle.delete(eintrag) #löscht alte Tabelle
        #MySQL abfrage
        cur.execute(f"""
            SELECT artikel.Artikelname, artikel.Lagerbestand, lieferant.Lieferantenname
            FROM artikel
            INNER JOIN lieferant ON artikel.Lieferant = lieferant.ID_lieferant
            WHERE artikel.Lagerbestand < {mindestmenge}
        """)

        artikelliste = [] #liste erstellt

        for (artikelname, lagerbestand, lieferantenname) in cur:
            artikel = Artikel(artikelname, lagerbestand, lieferantenname)
            artikelliste.append(artikel)

        # Artikel einfügen
        for artikel in artikelliste:
            tabelle.insert("", tk.END, values=(artikel.artikelname, artikel.lagerbestand, artikel.lieferantenname)) # Die .insert()-Methode fügt ein Element an einer bestimmten Stelle in einer Liste ein. Du sagst einfach, wo es hin soll, und die Liste schiebt die anderen Elemente nach hinten.

    except:
        print("Bitte eine gültige Zahl eingeben.")



#Erstellung des Fensters

# Fenster erstellen
fenster = tk.Tk()
fenster.title("Bestellung – Lagerabfrage")

# Eingabefeld
label = tk.Label(fenster, text="Mindeststückzahl:")
label.pack(pady=5)

eingabe_feld = tk.Entry(fenster)
eingabe_feld.pack(pady=5)

#Button Erstellen
button = tk.Button(fenster, text="Anzeigen", command=artikel_abfragen)
button.pack(pady=5)

#Tabelle erstellen
tabelle = ttk.Treeview(fenster, columns=("Name", "Lager", "Lieferant"), show="headings")
tabelle.heading("Name", text="Artikelname")
tabelle.heading("Lager", text="Lagerbestand")
tabelle.heading("Lieferant", text="Lieferant")

for spalte in tabelle["columns"]:
    tabelle.column(spalte, anchor="center") #zentrieren

tabelle.pack(fill=tk.BOTH, expand=True, pady=10)

# Fenster starten
fenster.mainloop()

# Verbindung schließen
cur.close()
conn.close()
