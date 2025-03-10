# Sujet 4 : Bus Allocation Problem (BAP)

Alexandre Louichon & Simon Hergott

Intervenant: Alexandre Saïdi

## Compréhension du problème

Entrée: un graphe, dont les arcs sont des routes et les noeuds sont des arrêts. De plus, on fournit un nombre k de lignes de bus pouvant circuler sur le graphe.

Sortie: Une optimisation du trajet pour chaque ligne de bus, de manière à minimiser le temps de trajet moyen d'un point à l'autre du graphe.

## Approche MACS:

Initialisation :
- Pour un problème avec n arrêts et m lignes de bus, on initialise un MACS avec m ACS.
- Chaque ACS contient r fourmis.

Construction des solutions :
- À chaque itération, chaque fourmi de chaque ACS construit une solution partielle (une ligne de bus).
- Les k-ièmes fourmis de chaque ACS collaborent pour construire une solution globale.
- La solution globale Sk est formée en combinant les solutions partielles de chaque ACS.
- Jk représente la liste des arrêts restant à visiter pour les k-ièmes fourmis.
- Lk et Lgb représentent les temps de parcours moyen.

Mise à jour des phéromones :
- Chaque ACS utilise une règle de mise à jour locale différente et une règle de mise à jour globale différente.
- Les mises à jour locales et globales des phéromones sont effectuées selon les équations 3.3, 3.4, 3.5 et 3.6.
- Cij représente la visibilité d'une arête, qui est l'inverse du temps de parcours entre deux arrêts.

Évaluation des solutions :
- La solution globale Sbg est la meilleure solution trouvée jusqu'à présent.
- Le temps de parcours moyen (att) de chaque solution est calculé.

## Explication globale

### Interface
L'interface est pilotée par interface.py, instanciée par main.py. On utilise une logique métier dans le back.py pour coordonner les actions: ce fichier gère la logique de l'interface (zone de dessin, boutons etc).

L'interface communique les actions au back, qui les communique à l'optimizer, qui lui même dicte à l'interface comment afficher certains éléments (architecture VMC).

### Optimizer
L'optimizer est le fichier principal faisant la liaison entre le problème d'allocation des bus, la classe des graphes de bus, les colonies de fourmis (acs.py), et les tests.

### Dernier gros commit Brams:
J'ai commencé à coder la logique pour plusieurs éléments du programme : le graphe d'une ligne de bus ainsi que la classe pour 1 colonie de fourmis.

Pour les fourmis, j'ai codé une fonction qui permet de choisir le prochain noeud exploré par la fourmi selon 2 possibilités : soit l'exploration (déposer des phéromones un peu partout puis choisir une direction un peu au hasard) soit l'exploitation (choix du noeud avec la meilleure visibilité et le plus fort taux de phéromones).

Il manque encore le code pour le dépôt et l'actualisation du dépôt de phéromones, et les deux fonctions de calcul dans select_next_nodes sont un peu placeholder (à changer).

Côté graphe bus, j'ai implémenté le graphe pour 1 bus, rien de bien spécial. L'idée sera ensuite d'avoir autant de graphes de bus que de lignes de bus pour lesquelles on cherche à optimiser le graphe global