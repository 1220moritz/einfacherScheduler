# Betriebssystem-Scheduler-Simulator
## Datenbereitstellung

### Eingabedatei

Die Prozesse, die vom Scheduler bearbeitet werden sollen, müssen in einer CSV-Datei mit dem Namen `Eingabe.csv` erfasst werden. Jede Zeile in dieser Datei repräsentiert einen Prozess und sollte drei Werte enthalten:

1. Prozess-ID: Eine eindeutige Identifikationsnummer für jeden Prozess.
2. Ankunftszeit: Die Zeit, zu der der Prozess im Scheduler eintrifft.
3. Laufzeit: Die Gesamtzeit, die der Prozess zur Ausführung benötigt.

Beispiel 1:
```
Prozess,Ankunftszeit,Laufzeit
1,0,9
2,15,4
3,8,13
4,10,3
5,12,7
```
Beispiel 2:
```
Prozess,Ankunftszeit,Laufzeit
1,3,5
2,0,10
3,5,2
4,9,7
5,13,3
```

### Scheduler-Konfiguration

Die Umschaltzeit, die der Scheduler zum Wechseln von einem Prozess zum anderen benötigt, wird vom Benutzer bei der Ausführung des Programms festgelegt. Diese Umschaltzeit wird bei der Berechnung der Start- und Endzeiten der Prozesse berücksichtigt.

## Scheduling-Algorithmen

Dieser Simulator bietet vier verschiedene Scheduling-Algorithmen zur Auswahl:

1. First Come First Serve (FCFS)
2. Non-Preemptive Shortest Job First (SJF)
3. Round Robin (RR)
4. Preemptive Shortest Job First (PSJF)

Jeder Algorithmus kann durch Eingabe der entsprechenden Zahl in der Konsole ausgewählt werden.

Für den Round-Robin-Algorithmus muss zusätzlich eine Zeitscheibe angegeben werden, die die Zeitdauer angibt, die jedem Prozess in jeder Runde zugewiesen wird.

## Ausführung und Ausgabe

Nach der Auswahl des Scheduling-Algorithmus und der Bereitstellung der notwendigen Parameter wird der Scheduler ausgeführt und die resultierenden Prozessdaten ausgegeben.

Die Ausgabe umfasst:

- Prozess-ID
- Ankunftszeit
- Laufzeit
- Startzeit
- Endzeit
- Verweilzeit
- Wartezeit
- Reaktionszeit
- Ø Verweilzeit, Ø Wartezeit, Ø Reaktionszeit, Ende

Diese Daten werden in der Konsole ausgegeben und zusätzlich in einer CSV-Datei mit dem Namen `Ausgabe.csv` gespeichert.

## Beenden des Simulators

Der Scheduler-Simulator wird nach jedem Durschlauf beendet.

