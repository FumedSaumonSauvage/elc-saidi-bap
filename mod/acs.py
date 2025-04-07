import numpy as np
import random
import math
from mod.graph import GlobalGraph, BusGraph
        
class Ant_Colony:
    def __init__(self, id_colony, nb_fourmis, graph, noeud_depart, noeud_arrivee,
                 qte_pheromones, alpha=1.0, beta=2.0, gamma=1.0, rho=0.1, q0=0.9, tau0=0.1, lignes_bus=None):
        self.id_colony = id_colony
        self.nb_fourmis = nb_fourmis
        self.graph = graph  # Type: GlobalGraph
        self.noeud_depart = noeud_depart
        self.noeud_arrivee = noeud_arrivee
        self.qte_pheromones = qte_pheromones
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.q0 = q0
        self.gamma = gamma  # Coefficient pour pénaliser les arcs partagés
        self.lignes_bus = lignes_bus  # Ajout des lignes de bus

        # Création des fourmis
        self.fourmis = [Ant(i, noeud_depart, noeud_arrivee, self) for i in range(nb_fourmis)]

        # Initialisation des niveaux de phéromones pour tous les arcs
        self.pheromones = {}
        for (n1, n2, _) in self.graph.arcs:
            key = (min(n1, n2), max(n1, n2))
            self.pheromones[key] = tau0

    def initialiser_fourmis(self):
        for fourmi in self.fourmis:
            fourmi.reset()

    def update_pheromones(self):
        # Mise à jour des phéromones sur les arcs
        for key in self.pheromones.keys():
            self.pheromones[key] *= (1 - self.rho) if self.rho < 1 else 0.0  # Évaporation des phéromones

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
                visibility = 1.0 / self.colonie.graph.get_arc(self.noeud_actuel, node)[2]  # Le poids représente le temps de trajet entre 2 noeuds
                pheromone = self.colonie.pheromones.get((min(self.noeud_actuel, node), max(self.noeud_actuel, node)), 0.1)
                
                # Ajout du facteur gamma pour pénaliser les arcs déjà utilisés par d'autres colonies
                gamma_penalty = 1.0
                for ligne_id, ligne_bus in self.colonie.lignes_bus.items():
                    if ligne_id != self.colonie.id_colony:  # Vérifie si la ligne appartient à une autre colonie
                        if ligne_bus.exists_arc(self.noeud_actuel, node):
                            gamma_penalty += self.colonie.gamma  # Augmente la pénalité pour chaque colonie étrangère utilisant cet arc
                
                # Calcul de la valeur d'attractivité avec pénalité gamma
                val = (pheromone ** self.colonie.alpha * visibility ** self.colonie.beta) / gamma_penalty
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

            temps_arc = self.colonie.graph.get_arc(self.noeud_actuel, next_node)[2] # temps == poids
            self.tps_trajet += temps_arc
            self.noeud_actuel = next_node
            self.visited.add(next_node)
            self.path.append(next_node)

            if next_node == self.noeud_cible:
                self.objectif = True

        if self.objectif:
            self.mettre_a_jour_pheromones()
        
    def mettre_a_jour_pheromones(self):
        # Calcule la qualité de la solution (inverse du temps de trajet)
        if self.tps_trajet > 0:
            ratio_pheromone = self.colonie.qte_pheromones / self.tps_trajet
            for i in range(len(self.path) - 1):
                n1 = self.path[i]
                n2 = self.path[i + 1]
                
                key = (min(n1, n2), max(n1, n2))
                qte = self.colonie.pheromones.get(key, 0.1) + ratio_pheromone * self.colonie.graph.get_arc(n1, n2)[2]
                self.colonie.pheromones[key] = qte