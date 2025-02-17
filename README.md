# Sujet 4 : Bus Allocation Problem (BAP)

Alexandre Louichon & Simon Hergott

Intervenant: Alexandre Saïdi

## Intro

Le Bus Allocation Problem (BAP) consiste à déterminer l'itinéraire optimal pour un ensemble de lignes de bus, chacune composée d'une liste d'arrêts. L'objectif est de minimiser le temps de trajet moyen des passagers.

Ce problème peut être abordé à l'aide d'un système de colonies de fourmis multiples (MACS), où chaque ligne de bus est représentée par une colonie de fourmis distincte.

## Description du problème

*   **Entrée :** Une liste de lignes de bus, chaque ligne étant composée d'une liste d'arrêts de bus.
*   **Sortie :** Un ensemble d'itinéraires pour les lignes de bus qui minimisent le temps de trajet moyen des passagers.

## Approche de résolution avec MACS

1.  **Représentation des lignes de bus :** Chaque ligne de bus est associée à une colonie de fourmis (ACS).
2.  **Construction des solutions :** Toutes les *k*-ièmes fourmis de chaque colonie construisent une solution ensemble, en choisissant les arrêts de bus à visiter en fonction des phéromones et de la visibilité des arêtes.
3.  **Mise à jour locale des phéromones :** Chaque ACS a une règle de mise à jour locale des phéromones différente.
4.  **Mise à jour globale des phéromones :** Chaque ACS a une règle de mise à jour globale des phéromones différente.
5.  **Évaluation des solutions :** Le temps de trajet moyen (ATT) de chaque solution est calculé à l'aide d'une matrice de transition (T) et d'une matrice de temps de trajet (U).
6.  **Amélioration des solutions :** Une extension du MACS peut être utilisée pour tenir compte du fait que certains arrêts de bus sont de meilleurs points de départ pour les lignes de bus que d'autres.

## Défis et considérations

*   **Choix des arrêts de départ :** Certains arrêts de bus peuvent être plus appropriés que d'autres pour démarrer une ligne de bus.
*   **Répartition des arrêts entre les lignes :** Il est important de s'assurer que les différentes lignes de bus ne desservent pas exactement les mêmes arrêts.
*   **Calcul du temps de trajet moyen :** Le calcul du temps de trajet moyen peut être complexe, car il nécessite de prendre en compte les temps de trajet entre les arrêts et les temps d'attente aux arrêts.

## Solutions potentielles

*   **Clustering des arrêts :** Les arrêts de bus peuvent être regroupés en fonction de critères géographiques, temporels, etc.
*   **Utilisation d'un arbre couvrant minimal (MST) :** Un MST peut être construit pour représenter les connexions entre les arrêts, puis divisé en sous-arbres pour former les itinéraires des lignes de bus.

## Conclusion

Le Bus Allocation Problem est un problème complexe qui peut être résolu à l'aide d'un système de colonies de fourmis multiples. L'approche MACS permet de prendre en compte les spécificités de chaque ligne de bus et de trouver des solutions optimisées pour minimiser le temps de trajet moyen des passagers.

N'hésitez pas à poser d'autres questions si vous souhaitez approfondir certains aspects du problème ou des solutions potentielles.