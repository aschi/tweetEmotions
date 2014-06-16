Seminararbeit: Erkennen von Emotionen in Tweets
==================================================================================
Diese Seminararbeit beschäftigt sich mit verschiedenen Algorithmen zur Erkennung von Emotionen in Tweets und deren Parallelisierung.

##Vorbereitungen:
1. Python pip installieren
2. MPI Installieren (mpiexec muss verfügbar sein)
3. pip install TwitterSearch
4. pip install sasa
5. pip install mpi4py
6. pip isntall matplotlib

##Verwendung:
1. Dateien herunterladen: git clone git@github.com:aschi/tweetEmotions.git
2. Ins src Verzeichnis wechseln: *cd tweetEmotions/src*
3. Starter ausführen: *python starter.py*

##Verzeichnisstruktur
- *doc*: Dokumentation. Enthält unter anderem Thesis (seminararbeit.pdf)
- *doc/content*: Latex Quelltext des Inhalts der Thesis
- *doc/images*: Verwendete Bilder in der Thesis
- *doc/sources*: Einige Papers die bei der Erstellung der Arbeit verwendet wurden
- *src/*: Sourcecode der Anwendung
- *src/starter.py*: Start Script der Anwendung
- *src/config*: Konfiguration des MPI Scripts
- *src/data*: Twitter Logdaten
- *src/logs*: Logfiles der durchgeführten Analysen
- *src/plots*: Plots der durchgeführten Analysen
- *src/res*: Verwendete Resourcen (SentiWordNet und SenticNet)
