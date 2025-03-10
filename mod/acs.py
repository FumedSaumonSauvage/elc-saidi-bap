import numpy as np
import random
import math

class AntColonySystem:
    def __init__(self, graph, colony_id, alpha=1.0, beta=2.0, rho=0.1, q0=0.9, tau0=None):
        """
        Initialise un système de colonie de fourmis pour une ligne de bus
        
        :param graph: Le graphe sur lequel les fourmis se déplacent, de classe GraphBus (doit avoir les fonctions get_node exist_edge et get_travel_time implémentées)
        :param colony_id: Identifiant de la colonie
        :param alpha: Importance des phéromones
        :param beta: Importance de la visibilité (inverse du temps de parcours)
        :param rho: Taux d'évaporation des phéromones
        :param q0: Paramètre d'exploration/exploitation
        :param tau0: Valeur initiale des phéromones
        """
        self.graph = graph
        self.colony_id = colony_id
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.q0 = q0
        
        # Initialisation des phéromones
        self.pheromones = {}
        for i in graph.get_nodes():
            for j in graph.get_nodes():
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