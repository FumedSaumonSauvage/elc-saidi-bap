import numpy as np
import random
import math
from mod.graph import GlobalGraph, BusGraph
        
class Ant_Colony:
    def __init__(self, id_colony, nb_fourmis, graph, noeud_depart, noeud_arrivee,
                 qte_pheromones, alpha=1.0, beta=2.0, rho=0.1, q0=0.9, tau0=0.1):
        self.id_colony = id_colony
        self.nb_fourmis = nb_fourmis
        self.graph = graph
        self.noeud_depart = noeud_depart
        self.noeud_arrivee = noeud_arrivee
        self.qte_pheromones = qte_pheromones

        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.q0 = q0

        # Création des fourmis
        self.fourmis = [Ant(i, noeud_depart, noeud_arrivee, self) for i in range(nb_fourmis)]

        # Initialisation des niveaux de phéromones pour tous les arcs
        self.pheromones = {}
        for i in graph.get_nodes():
            for j in graph.get_neighbors(i):
                if (i, j) not in self.pheromones:
                    self.pheromones[(i, j)] = tau0

    def initialiser_fourmis(self):
        for fourmi in self.fourmis:
            fourmi.reset()


class Ant:
    def __init__(self, id_fourmi, noeud_initial, noeud_cible, colonie):
        self.colonie = colonie
        self.objectif = False
        self.noeud_initial = noeud_initial
        self.noeud_cible = noeud_cible
        self.id_fourmi = id_fourmi

        self.noeud_actuel = noeud_initial
        self.path = [noeud_initial]
        self.visited = set([noeud_initial])
        self.tps_trajet = 0.0

    def reset(self):
        self.objectif = False
        self.noeud_actuel = self.noeud_initial
        self.path = [self.noeud_initial]
        self.visited = set([self.noeud_initial])
        self.tps_trajet = 0.0

    def voisins(self):
        # Récupère les voisins accessibles et non visités
        return set(self.colonie.graph.get_neighbors(self.noeud_actuel)) - self.visited

    def choix_noeud(self):
        voisins = self.voisins()
        if not voisins:
            return None

        q = random.random()
        if q <= self.colonie.q0:  # Exploitation
            max_val = -float('inf')
            next_node = None
            for node in voisins:
                arc = self.colonie.graph.exists_arc(self.noeud_actuel, node)
                if arc:
                    visibility = 1.0 / arc[2]
                    pheromone = self.colonie.pheromones.get((self.noeud_actuel, node), 0.1)
                    val = pheromone ** self.colonie.alpha * visibility ** self.colonie.beta
                    if val > max_val:
                        max_val = val
                        next_node = node
            return next_node
        else:  # Exploration
            return random.choice(list(voisins))

    def deplacement(self):
        while not self.objectif and self.voisins():
            next_node = self.choix_noeud()
            if next_node is None:
                break

            arc = self.colonie.graph.exists_arc(self.noeud_actuel, next_node)
            self.tps_trajet += arc[2]
            self.noeud_actuel = next_node
            self.visited.add(next_node)
            self.path.append(next_node)

            if next_node == self.noeud_cible:
                self.objectif = True

        if self.objectif:
            ratio_pheromone = self.colonie.qte_pheromones / self.tps_trajet
            for i in range(len(self.path) - 1):
                n1 = self.path[i]
                n2 = self.path[i + 1]
                arc = self.colonie.graph.exists_arc(n1, n2)
                if arc:
                    self.colonie.pheromones[(n1, n2)] += ratio_pheromone * arc[2]
