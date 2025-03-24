import math
import numpy as np

class BusGraph:
    # Classe qui décrit un graphe pour un bus en particulier
    # L'ensemble des graphes des lignes (joints) forme le graphe global

    def __init__(self):
        """
            Initialise un graphe pour ce bus en particulier (ligne de bus)
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
    
    def get_nodes(self): return self.noeuds
    
    def get_travel_time(self, node1, node2):
        """
            Par construction, un arc entre deux noeuds est de la forme suivante :
            (n1, n2, temps_parcours)
        """ 
        # Convention, si l'arête n'existe pas, on retourne infini (pas fou de manipuler l'infini mais il peut y avoir des grandes distances)
        for arc in self.arcs:
            if arc[0] == node1 and arc[1] == node2:
                return arc[2]
        return float('inf')
    
    def exists_edge(self, node1, node2):
        return any(arc[0] == node1 and arc[1] == node2 for arc in self.arcs)
    
    def from_dict(self, nodes_dict, arcs_list):
        """
            On crée le graphe de la ligne de bus à partir d'un dico de noeuds et d'une liste d'arêtes
        """
        self.noeuds = {}
        self.arcs = []

        for node_id, (x, y) in nodes_dict.items():
            self.add_node(int(node_id), x, y)

        # Attention à la convention de l'arête : (node1, node2, tps_parcours)
        for node1, node2, tps_parcours in arcs_list:
            self.add_edge(node1, node2, tps_parcours)
            self.add_edge(node2, node1, tps_parcours) 
            # On fait un graphe non orienté. A discuter sur ce point là en particulier 
            # mais je pense que c'est plus simple d'ajouter de la symétrie dans la recherche d'arcs de connexion entre deux noeuds

class GlobalGraph:
    # Classe qui décrit le graphe global "vierge" (sans les lignes de bus)
    # On peut donc considérer que c'est un graphe non orienté.

    def __init__(self, nodes, arcs):
        """
            Initialise le graphe global
            nodes: format {id_noeud: (x, y)}
            arcs: format [(id_noeud1, id_noeud2, temps_parcours)]
        """
        self.nodes = nodes
        self.arcs = arcs 
    
    def exists_edge(self, node1, node2):
        """
            Vérifie si une arête existe entre deux nœuds dans le graphe global (ie : il existe au moins une ligne de bus qui relie les deux noeuds)
        """
        return any(bus_graph.exists_edge(node1, node2) for _, bus_graph in self.graphes.items())
    
    def from_dict(self, graph_dict):
        """
            On crée le graphe global à partir d'un dico : graph_dict qui contient :
                - les noms des lignes de bus
                - les dicos des noeuds de chaque ligne
                - les listes d'arêtes de chaque ligne
        """
        self.graphes = {}
        for line_id, (nodes_dict, arcs_list) in graph_dict.items():
            bus_graph = BusGraph()
            bus_graph.from_dict(nodes_dict, arcs_list)
            self.add_graph(line_id, bus_graph)

    def are_arcs_contingent(self, arc1, arc2):
        """
            Vérifie si deux arcs sont contigus (ie : ils partagent un nœud en commun)
        """
        return arc1[0] == arc2[0] or arc1[0] == arc2[1] or arc1[1] == arc2[0] or arc1[1] == arc2[1]
    
    def get_contingent_nodes(self, noeud):
        """
            Retourne les noeuds contigus à un nœud donné
        """
        return [arc[0] if arc[1] == noeud else arc[1] for _, bus_graph in self.graphes.items() for arc in bus_graph.arcs if noeud in arc]


