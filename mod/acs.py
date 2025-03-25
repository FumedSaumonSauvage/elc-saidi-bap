import numpy as np
import random
import math
from mod.graph import GlobalGraph, BusGraph
        
class Ant_Colony:
    def __init__(self, id_colony, nb_fourmis, graph, noeud_depart, noeud_arrivee, qte_pheromones, alpha=1.0, beta=2.0, rho=0.1, q0=0.9, tau0=None):
        self.id_colony = id_colony
        self.nb_fourmis = nb_fourmis
        self.graph = GlobalGraph()
        self.graph.from_dict(graph)
        self.fourmis = [Ant(i, noeud_depart, noeud_arrivee, self) for i in range(nb_fourmis)]
        self.pheromones = {}
        for i in self.graph.get_nodes().keys():
            for j in self.graph.get_nodes().keys():
                if i != j and self.graph.exists_edge(i, j):
                    self.pheromones[(i, j)] = tau0 if tau0 else 0.1
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.q0 = q0
        self.qte_pheromones = qte_pheromones
        

class Ant:
    def __init__(self, id_fourmi, noeud_initial, noeud_cible, colonie):
        self.objectif = False
        self.noeud_actuel = noeud_initial
        self.noeud_cible = noeud_cible
        self.id_fourmi = id_fourmi
        self.visites = {noeud_initial: True}
        self.a_visiter = set()
        self.colonie = colonie
        self.tps_trajet = 0.0 # Paramètre qui permet de savoir la distance parcourue par la fourmi pour pouvoir distribuer les phéromones de manière homogène par la suite

    def voisins(self):
        return self.colonie.graph.get_contingent_nodes(self.noeud_actuel)
    
    def choix_noeud(self):
        """
            Sélectionne le prochain nœud en utilisant la règle de transition d'état ACS : 
                - Exploitation : Choisir le nœud avec la plus grande valeur de phéromones et visibilité
                - Exploration : Choisir un nœud aléatoire parmi les noeuds voisins
        """
        if not self.a_visiter:
            return None
        
        # Choix aléatoire entre exploitation et exploration (basé sur q0)
        q = random.random()
        if q <= self.colonie.q0:  # Exploitation
            max_val = -float('inf')
            next_node = None
            for node in self.a_visiter:
                if self.colonie.graph.exists_edge(self.noeud_actuel, node):
                    # Calcul de la visibilité (inverse du temps de parcours)
                    visibility = 1.0 / self.colonie.graph.exists_edge(self.noeud_actuel, node)[2]

                    # Le calcul de cette valeur dépend de la fonction qui a été choisie (cf enoncé)
                    val = self.pheromones.get((self.noeud_actuel, node), 0) ** self.alpha * visibility ** self.beta

                    # Algo de max pour déterminer le prochain noeud avec le plus de phéromones
                    if val > max_val:
                        max_val = val
                        next_node = node
            return next_node
        else:  # Exploration
            return random.choice([n for n in self.a_visiter if self.colonie.graph.exists_edge(self.noeud_actuel, n)]) if self.a_visiter else None

    # Fonction de déplacement de la fourmi
    def deplacement(self):
        while self.a_visiter and not self.objectif:
            # On choisit le prochain noeud à visiter
            # Normalement on est sûr que la fonction choix_node renverra un voisin car si on est dans un cul de sac 
            # par définition de la condition de sortie du while on n'appellera pas à nouveau la fonction choix_node
            nouveau_noeud = self.choix_node()
            self.tps_trajet += self.graph.exists_edge(self.noeud_actuel, nouveau_noeud)[2]
            self.noeud_actuel = nouveau_noeud
            self.a_visiter = self.voisins()
            self.visites[self.noeud_actuel] = True
            self.objectif = self.noeud_actuel == self.noeud_cible

        # Une fois sorti du while, il y a deux possibilités : soit on n'a plus de noeuds à visiter (cul de sac) soit on a atteint le noeud objectif
        # On ne dépose de phéromone que sur un chemin pour lequel on a atteint l'objectif
        if self.objectif:
            # On dépose la quantité de phéromones attribué pour chaque fourmi de manière proportionnelle à la distance parcourue entre chaque noeud
            ratio_pheromone = self.colonie.qte_pheromones / self.tps_trajet
            for n1 in self.visites.keys():
                for n2 in self.visites.keys():
                    if n1 != n2 and self.colonie.graph.exists_edge(n1, n2):
                        self.colonie.pheromones[(n1, n2)] += ratio_pheromone * self.graph.exists_edge(n1, n2)[2]

