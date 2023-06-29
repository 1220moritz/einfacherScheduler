# -*- coding: utf-8 -*-
import csv

class Prozess:
    def __init__(self, prozess_id: int, ankunftszeit: float, laufzeit: float):
        self.prozess_id = prozess_id
        self.ankunftszeit = ankunftszeit
        self.laufzeit = laufzeit

        self.verbleibende_zeit = None
        
        self.startzeit = None
        self.endzeit = None
        self.verweilzeit = None
        self.wartezeit = None
        self.reaktionszeit = None

    def __str__(self):
        return f'Prozess ID: {self.prozess_id}\n' \
               f'Ankunftszeit: {self.ankunftszeit}\n' \
               f'Laufzeit: {self.laufzeit}\n' \
               f'Startzeit: {self.startzeit}\n' \
               f'Endzeit: {self.endzeit}\n' \
               f'Verweilzeit: {self.verweilzeit}\n' \
               f'Wartezeit: {self.wartezeit}\n' \
               f'Reaktionszeit: {self.reaktionszeit}\n'


# Schedulerklasse zur Verwaltung der Prozesse
class Scheduler:
    prozess_tabelle = [] # Liste aller Prozesse
    fertige_prozesse = [] # Liste aller fertiggestellten Prozesse
    umschaltzeit = None

    def __init__(self):
        self.prozess_tabelle_einlesen()

    def __str__(self):
        output = ""
        for prozess in self.fertige_prozesse:
            output += str(prozess) + "\n"
        return output
    
    def ausgabe(self):
        vergleichsdaten: tuple = self.vergleichsdaten_berechnen()
        augabeString: str = self.__str__()
        augabeString += f"Ø Verweilzeit: {vergleichsdaten[1]}, Ø Wartezeit: {vergleichsdaten[2]}, Ø Reaktionszeit: {vergleichsdaten[3]}, Ende: {vergleichsdaten[0]}"
        with open("Ausgabe.csv", 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Prozess ID", "Ankunftszeit", "Laufzeit", "Startzeit", "Endzeit", "Verweilzeit", "Wartezeit", "Reaktionszeit"])
            for prozess in self.fertige_prozesse:
                writer.writerow([prozess.prozess_id, prozess.ankunftszeit, prozess.laufzeit, prozess.startzeit, prozess.endzeit, prozess.verweilzeit, prozess.wartezeit, prozess.reaktionszeit])
            writer.writerow(["", "", "", "", "Ende", "Ø Verweilzeit", "Ø Wartezeit", "Ø Reaktionszeit"])
            writer.writerow(["", "", "", "", vergleichsdaten[0], vergleichsdaten[1], vergleichsdaten[2], vergleichsdaten[3]])
            
                
        self.prozess_tabelle = []
        self.fertige_prozesse = []
        self.umschaltzeit = None
        
        return augabeString
    
    def prozess_tabelle_einlesen(self):
        """
        Liest die Prozesstabelle aus der Datei "eingabe.csv" ein und speichert sie in der Prozessliste
        """
        with open("eingabe.csv", 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Header ignorieren

            for zeile in reader:
                temp_prozess = Prozess(int(zeile[0]), float(zeile[1]), float(zeile[2]))
                self.prozess_tabelle.append(temp_prozess)
                
                
    def vergleichsdaten_berechnen(self):
        counter: int = 0
        durchschnitt_verweilzeit: float = 0
        durschnitt_warzeit: float = 0
        durschnitt_reaktionszeit: float = 0
        finale_endzeit: float = 0
        
        for prozess in self.fertige_prozesse:
            counter += 1
            durchschnitt_verweilzeit += prozess.verweilzeit
            durschnitt_warzeit += prozess.wartezeit
            durschnitt_reaktionszeit += prozess.reaktionszeit
            
            if prozess.endzeit > finale_endzeit:
                finale_endzeit = prozess.endzeit
        
        durchschnitt_verweilzeit /= counter
        durschnitt_warzeit /= counter
        durschnitt_reaktionszeit /= counter
        
        return finale_endzeit, durchschnitt_verweilzeit, durschnitt_warzeit, durschnitt_reaktionszeit
            
        

    def fcfs(self):
        """
        First Come First Serve Algorithmus
        """
        aktuelle_zeit = 0
        start_periode = None
        ende_periode = None
        # Sortiere die Prozesstabelle nach Ankunftszeit
        self.prozess_tabelle.sort(key=lambda prozess: prozess.ankunftszeit)
        prozesse_zur_verarbeitung = self.prozess_tabelle.copy()

        for prozess in prozesse_zur_verarbeitung:
            start_periode = aktuelle_zeit
            if prozess.ankunftszeit > aktuelle_zeit:
                aktuelle_zeit = prozess.ankunftszeit

            prozess.startzeit = aktuelle_zeit
            prozess.endzeit = aktuelle_zeit + prozess.laufzeit
            prozess.verweilzeit = prozess.endzeit - prozess.ankunftszeit
            prozess.reaktionszeit = prozess.startzeit - prozess.ankunftszeit
            prozess.wartezeit = prozess.verweilzeit - prozess.laufzeit

            aktuelle_zeit = prozess.endzeit
            ende_periode = aktuelle_zeit
            self.fertige_prozesse.append(prozess)
            self.prozess_tabelle.remove(prozess)
            
            print(f"Prozess {prozess.prozess_id} wurde von {start_periode} bis {ende_periode} verarbeitet")
                # Umschaltzeit hinzufügen, außer es ist der letzte Prozess
            if self.prozess_tabelle:
                aktuelle_zeit += self.umschaltzeit


    def non_preemptive_shortest_job_first(self):
        """
        Non-Preemptive Shortest Job First Algorithmus
        """
        aktuelle_zeit = 0
        start_periode = None
        ende_periode = None
        # Sortiere die Prozesstabelle nach Ankunftszeit
        self.prozess_tabelle.sort(key=lambda prozess: prozess.ankunftszeit)
        
        while self.prozess_tabelle:
            ankommende_prozesse = [prozess for prozess in self.prozess_tabelle if prozess.ankunftszeit <= aktuelle_zeit]
            if not ankommende_prozesse:
                aktuelle_zeit += 1
                continue

            kuerzester_prozess = min(ankommende_prozesse, key=lambda prozess: prozess.laufzeit)

            start_periode = aktuelle_zeit
            kuerzester_prozess.startzeit = aktuelle_zeit
            kuerzester_prozess.reaktionszeit = kuerzester_prozess.startzeit - kuerzester_prozess.ankunftszeit

            aktuelle_zeit += kuerzester_prozess.laufzeit
            kuerzester_prozess.endzeit = aktuelle_zeit
            kuerzester_prozess.verweilzeit = kuerzester_prozess.endzeit - kuerzester_prozess.ankunftszeit
            kuerzester_prozess.wartezeit = kuerzester_prozess.verweilzeit - kuerzester_prozess.laufzeit
            ende_periode = aktuelle_zeit
            
            self.fertige_prozesse.append(kuerzester_prozess)
            self.prozess_tabelle.remove(kuerzester_prozess)
            
            print(f"Prozess {kuerzester_prozess.prozess_id} wurde von {start_periode} bis {ende_periode} verarbeitet")
                # Umschaltzeit hinzufügen, außer es ist der letzte Prozess
            if self.prozess_tabelle:
                aktuelle_zeit += self.umschaltzeit
            
            
    def round_robin(self, zeitscheibe: int):
        """
        Round Robin Algorithmus

        :param zeitscheibe: Zeitscheibe in s
        """
        aktuelle_zeit = 0
        start_periode = None
        ende_periode = None
        # Sortiere die Prozesstabelle nach Ankunftszeit
        self.prozess_tabelle.sort(key=lambda prozess: prozess.ankunftszeit)
        laufende_prozesse = []

        while self.prozess_tabelle or laufende_prozesse:
            ankommende_prozesse = [prozess for prozess in self.prozess_tabelle if prozess.ankunftszeit <= aktuelle_zeit]

            laufende_prozesse += ankommende_prozesse
            for prozess in ankommende_prozesse:
                self.prozess_tabelle.remove(prozess)

            if not laufende_prozesse:
                aktuelle_zeit += 1
                continue

            aktueller_prozess = laufende_prozesse.pop(0)

            start_periode = aktuelle_zeit
            if aktueller_prozess.verbleibende_zeit is None:  # Prozess startet
                aktueller_prozess.startzeit = aktuelle_zeit
                aktueller_prozess.verbleibende_zeit = aktueller_prozess.laufzeit
                aktueller_prozess.reaktionszeit = aktueller_prozess.startzeit - aktueller_prozess.ankunftszeit

            if aktueller_prozess.verbleibende_zeit > zeitscheibe:  # Prozess läuft für die Dauer der Zeitscheibe
                aktuelle_zeit += zeitscheibe
                aktueller_prozess.verbleibende_zeit -= zeitscheibe
                laufende_prozesse.append(aktueller_prozess)
            else:  # Prozess läuft bis zum Ende
                aktuelle_zeit += aktueller_prozess.verbleibende_zeit
                aktueller_prozess.endzeit = aktuelle_zeit
                aktueller_prozess.verweilzeit = aktueller_prozess.endzeit - aktueller_prozess.ankunftszeit
                aktueller_prozess.wartezeit = aktueller_prozess.verweilzeit - aktueller_prozess.laufzeit
                self.fertige_prozesse.append(aktueller_prozess)
            
            ende_periode = aktuelle_zeit
            print(f"Prozess {aktueller_prozess.prozess_id} wurde von {start_periode} bis {ende_periode} verarbeitet")
            # Umschaltzeit hinzufügen, außer es ist der letzte Prozess
            if self.prozess_tabelle or laufende_prozesse:
                aktuelle_zeit += self.umschaltzeit


            
            
    def preemptive_shortest_job_first(self):
        """
        Preemptive Shortest Job First Algorithmus
        """
        aktuelle_zeit = 0
        start_periode = None
        ende_periode = None
        # Sortiere die Prozesstabelle nach Ankunftszeit
        self.prozess_tabelle.sort(key=lambda prozess: prozess.ankunftszeit)
        laufende_prozesse = []

        while self.prozess_tabelle or laufende_prozesse:
            ankommende_prozesse = [prozess for prozess in self.prozess_tabelle if prozess.ankunftszeit <= aktuelle_zeit]

            laufende_prozesse += ankommende_prozesse
            for prozess in ankommende_prozesse:
                self.prozess_tabelle.remove(prozess)

            if not laufende_prozesse:
                aktuelle_zeit += 1
                continue

            kuerzester_prozess = min(laufende_prozesse, key=lambda prozess: prozess.laufzeit if prozess.verbleibende_zeit is None else prozess.verbleibende_zeit)

            start_periode = aktuelle_zeit
            if kuerzester_prozess.verbleibende_zeit is None:  # Prozess startet
                kuerzester_prozess.startzeit = aktuelle_zeit
                kuerzester_prozess.verbleibende_zeit = kuerzester_prozess.laufzeit - 1
                kuerzester_prozess.reaktionszeit = kuerzester_prozess.startzeit - kuerzester_prozess.ankunftszeit
            else:  # Prozess wird fortgesetzt
                kuerzester_prozess.verbleibende_zeit -= 1

            ende_periode = aktuelle_zeit
            if kuerzester_prozess.verbleibende_zeit == 0:  # Prozess ist abgeschlossen
                aktuelle_zeit += 1
                kuerzester_prozess.endzeit = aktuelle_zeit
                kuerzester_prozess.verweilzeit = kuerzester_prozess.endzeit - kuerzester_prozess.ankunftszeit
                kuerzester_prozess.wartezeit = kuerzester_prozess.verweilzeit - kuerzester_prozess.laufzeit
                self.fertige_prozesse.append(kuerzester_prozess)
                laufende_prozesse.remove(kuerzester_prozess)
            else:
                aktuelle_zeit += 1
                # Addiere Umschaltzeit, wenn es einen weiteren laufenden Prozess gibt
                if len(laufende_prozesse) > 1:
                    aktuelle_zeit += self.umschaltzeit
            
            print(f"Prozess {kuerzester_prozess.prozess_id} wurde von {start_periode} bis {ende_periode} verarbeitet")

        







if __name__ == '__main__': 
    scheduler = Scheduler()
        
    scheduler.umschaltzeit = int(input("Umschaltzeit: "))

    auswahl: int = int(input("\n1: FCFS\n2: SJF\n3: RoundRobin\n4: PSJF\n5: Exit\n\nAuswahl: "))
    if auswahl == 1:
        scheduler.fcfs()
    elif auswahl == 2:
        scheduler.non_preemptive_shortest_job_first()
    elif auswahl == 3:
        zeitscheibe: int = None
        while zeitscheibe is None:
            try:
                eingabe = int(input("Zeitscheibe: "))
            except ValueError:
                print("Ungültige Zeitscheibe -> Bitte eine Zahl eingeben")
                continue
                    
            if eingabe < 1:
                print("Ungültige Zeitscheibe -> Bitte eine Zahl größer 0 eingeben")
                continue
            else:
                zeitscheibe = eingabe
                break
                
        scheduler.round_robin(zeitscheibe)
    elif auswahl == 4:
        scheduler.preemptive_shortest_job_first()
    elif auswahl == 5:
        exit(0)
    else:
        print("Ungültige Auswahl")

    print("\n" + scheduler.ausgabe())
