import numpy as np
import random
import math
from mod.graph import GlobalGraph, BusGraph

class AntColonySystem:
    def __init__(self, graph, colony_id, alpha=1.0, beta=2.0, rho=0.1, q0=0.9, tau0=None):
        """
         Initialise un sys
        """
        self.graph = graph
        self.colony_id = colony_id
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.q0 = q0
        
        # Initialisation des phéromones pour la colonie de fourmis, avec des phéromones initiales tau0 sur les arêtes qui existent
        self.pheromones = {}
        for i in graph.get_nodes().keys():
            for j in graph.get_nodes().keys():
                if i != j and graph.exists_edge(i, j):
                    self.pheromones[(i, j)] = tau0 if tau0 else 0.1

    def select_next_node(self, current_node, unvisited_nodes):
        """
            Sélectionne le prochain nœud en utilisant la règle de transition d'état ACS : 
                - Exploitation : Choisir le nœud avec la plus grande valeur de phéromones et visibilité
                - Exploration : Choisir un nœud aléatoire en fonction des probabilités calculées
        """
        if not unvisited_nodes:
            return None
        
        # Choix aléatoire entre exploitation et exploration (basé sur q0)
        q = random.random()
        if q <= self.q0:  # Exploitation
            max_val = -float('inf')
            next_node = None
            for node in unvisited_nodes:
                if self.graph.exists_edge(current_node, node):
                    # Calcul de la visibilité (inverse du temps de parcours)
                    visibility = 1.0 / self.graph.get_travel_time(current_node, node)

                    # Le calcul de cette valeur dépend de la fonction qui a été choisie (cf enoncé)
                    val = self.pheromones.get((current_node, node), 0) ** self.alpha * visibility ** self.beta

                    # Algo de max pour déterminer le prochain noeud avec le plus de phéromones
                    if val > max_val:
                        max_val = val
                        next_node = node
            return next_node
        else:  # Exploration
            total = 0
            probabilities = {}
            for node in unvisited_nodes:
                if self.graph.exists_edge(current_node, node):
                    # Meme méthode de calcul de visibilité que pour l'exploitation
                    visibility = 1.0 / self.graph.get_travel_time(current_node, node)

                    # Pas sur non plus de cette fonction pour le calcul de la probabilité
                    probabilities[node] = self.pheromones.get((current_node, node), 0) ** self.alpha * visibility ** self.beta
                    total += probabilities[node]
            
            # Aucune phéromone n'a été déposée sur les nœuds voisins
            if total == 0:
                return random.choice([n for n in unvisited_nodes if self.graph.exists_edge(current_node, n)]) if unvisited_nodes else None
            
            # On choisit un noeud aléatoire en fonction des probabilités calculées
            r = random.random() * total
            somme = 0
            for node, probability in probabilities.items():
                somme += probability
                if somme >= r:
                    return node
            
            return next(iter(unvisited_nodes))  # Fallback --> utilisé le chat là dessus mais pas trop compris pk
        
class Ant_Colony:
    def __init__(self, id_colony, nb_fourmis, graph):
        self.id_colony = id_colony
        self.nb_fourmis = nb_fourmis
        self.graph = GlobalGraph()
        self.graph.from_dict(graph)
        # self.fourmis = [Ant(i, graph.get_random_node(), graph.get_random_node(), self) for i in range(nb_fourmis)]
        

class Ant:
    def __init__(self, id_fourmi, noeud_initial, noeud_cible, colonie):
        self.objectif = False
        self.noeud_actuel = noeud_initial
        self.noeud_cible = noeud_cible
        self.id_fourmi = id_fourmi
        self.visites = {noeud_initial: True}
        self.a_visiter = set()
        self.colonie = colonie
        self.pheromones = {} # TODO : formaliser

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
        if q <= self.q0:  # Exploitation
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
        else:  # Exploration -> return random
            total = 0
            probabilities = {}
            for node in self.a_visiter:
                if self.colonie.graph.exists_edge(self.noeud_actuel, node):
                    # Meme méthode de calcul de visibilité que pour l'exploitation
                    visibility = 1.0 / self.graph.get_travel_time(self.noeud_actuel, node)[2]

                    # Pas sur non plus de cette fonction pour le calcul de la probabilité
                    probabilities[node] = self.pheromones.get((self.noeud_actuel, node), 0) ** self.alpha * visibility ** self.beta
                    total += probabilities[node]
            
            # Aucune phéromone n'a été déposée sur les nœuds voisins
            if total == 0:
                return random.choice([n for n in self.a_visiter if self.colonie.graph.exists_edge(self.noeud_actuel, n)]) if self.a_visiter else None
            
            # On choisit un noeud aléatoire en fonction des probabilités calculées
            r = random.random() * total
            somme = 0
            for node, probability in probabilities.items():
                somme += probability
                if somme >= r:
                    return node
            
            return next(iter(self.a_visiter))


    # Fonction de déplacement de la fourmi
    def deplacement(self):
        while self.a_visiter and not self.objectif:
            # On choisit le prochain noeud à visiter
            self.noeud_actuel = self.choix_noeud()
            self.a_visiter = self.voisins()
            self.visites[self.noeud_actuel] = True
            self.objectif = self.noeud_actuel == self.noeud_cible

        # Une fois sorti du while, il y a deux possibilités : soit on n'a plus de noeuds à visiter (cul de sac) soit on a atteint le noeud objectif
        # On ne dépose de phéromone que sur un chemin pour lequel on a atteint l'objectif
        if self.objectif:
            # On dépose la quantité de phéromones attribué pour chaque fourmi de manière proportionnelle à la distance parcourue entre chaque noeud
            # TODO : formaliser les phéromones
            pass

