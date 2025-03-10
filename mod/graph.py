import math
import numpy as np

class BusGraph:
    # Classe qui décrit un graphe pour un bus en particulier
    # L'ensemble des graphes des lignes (joints) forment le graphe global

    def __init__(self):
        """
            Initialise un graphe pour ce bus en particulier 
            (il faudra l'étendre avec les autres graphes des autres bus pour ensuite pouvoir recouvrir le graphe global)
        """
        self.noeuds = {}  # id: (x, y)
        self.arcs = []  # (id_noeud1, id_noeud2)
    
    def add_node(self, node_id, x, y):
        """
            Ajoute un nœud au graphe
        """
        self.noeuds[node_id] = (x, y)
    
    def add_edge(self, node1, node2):
        """
            Ajoute une arête entre deux nœuds
        """
        # On vérifie qu'il existe bien les deux noeuds ainsi que l'arête qui les relie
        if not self.exists_edge(node1, node2) and node1 in self.noeuds and node2 in self.noeuds:
            # Calcule le temps de parcours basé sur la distance euclidienne (classique)
            x1, y1 = self.noeuds[node1]
            x2, y2 = self.noeuds[node2]

            temps_parcours = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            self.arcs.append((node1, node2, temps_parcours))
            self.arcs.append((node2, node1, temps_parcours))  # --> Le graphe n'est pas orienté
    
    def get_nodes(self):
        return self.noeuds
    
    def get_travel_time(self, node1, node2): 
        # Convention, si l'arête n'existe pas, on retourne infini (pas fou de manipuler l'infini mais il peut y avoir des grandes distances)
        for arc in self.arcs:
            if arc[0] == node1 and arc[1] == node2:
                return arc[2]
        return float('inf')
    
    def exists_edge(self, node1, node2):
        return any(arc[0] == node1 and arc[1] == node2 for arc in self.arcs)
    
    def from_dict(self, nodes_dict, arcs_list): # TODO : vérifier si cette fonction colle avec la définition des graphes comme dans back.py
        """
            On crée le graphe à partir d'un dico : nodes_dict et d'une listes d'arêtes : arcs_list
        """
        self.noeuds = {}
        self.arcs = []

        for node_id, (x, y) in nodes_dict.items():
            self.add_node(int(node_id), x, y)
    
        for node1, node2 in arcs_list:
            self.add_edge(node1, node2)

class GlobalGraph:
    # Classe qui décrit le graphe global, c'est à dire l'ensemble des lignes de bus
    # On peut donc considérer que c'est un graphe non orienté

    def __init__(self):
        """
            Initialise le graphe global
        """
        self.graphes = {}  # id_ligne: BusGraph
    
    def add_graph(self, line_id, bus_graph):
        """
            Ajoute un graphe de ligne au graphe global
        """
        self.graphes[line_id] = bus_graph
    
    def get_nodes(self):
        return {line_id: bus_graph.get_nodes() for line_id, bus_graph in self.graphes.items()}
    
    def get_travel_time(self, node1, node2):
        """
            Retourne le temps de parcours entre deux nœuds
        """
        # On cherche le temps de parcours le plus court entre les deux nœuds
        travel_times = []
        for _, bus_graph in self.graphes.items():
            travel_times.append(bus_graph.get_travel_time(node1, node2))
        
        return min(travel_times)
    
    def exists_edge(self, node1, node2):
        """
            Vérifie si une arête existe entre deux nœuds
        """
        return any(bus_graph.exists_edge(node1, node2) for _, bus_graph in self.graphes.items())
    
    def from_dict(self, graph_dict):
        """
            On crée le graphe global à partir d'un dico : graph_dict
        """
        self.graphes = {}
        for line_id, (nodes_dict, arcs_list) in graph_dict.items():
            bus_graph = BusGraph()
            bus_graph.from_dict(nodes_dict, arcs_list)
            self.add_graph(line_id, bus_graph)
