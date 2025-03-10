import math
import numpy as np

class BusGraph:
    def __init__(self):
        """
            Initialise un graphe pour ce bus en particulier 
            (il faudra l'étendre avec les autres graphes des autres bus pour ensuite pouvoir recouvrir le graphe global)
        """
        self.nodes = []  # Ensemble des nœuds (arrêts de bus)
        self.edges = {}  # Dictionnaire des arêtes {(noeud1, noeud2): temps_parcours}
        self.positions = {}  # Positions des nœuds {noeud: (x, y)}
    
    def add_node(self, node_id, x, y):
        """
            Ajoute un nœud au graphe
        """
        self.nodes.add(node_id)
        self.positions[node_id] = (x, y)
    
    def add_edge(self, node1, node2):
        """
            Ajoute une arête entre deux nœuds
        """
        # On vérifie qu'il existe bien les deux noeuds ainsi que l'arête qui les relie
        if not self.exists_edge(node1, node2) and node1 in self.nodes and node2 in self.nodes: return
        
        
        # Calcule le temps de parcours basé sur la distance euclidienne (classique)
        x1, y1 = self.positions[node1]
        x2, y2 = self.positions[node2]

        temps_parcours = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        self.edges[(node1, node2)] = temps_parcours
        self.edges[(node2, node1)] = temps_parcours  # --> Le graphe n'est pas orienté
    
    def get_nodes(self): return self.nodes
    
    def get_travel_time(self, node1, node2): 
        # Convention, si l'arête n'existe pas, on retourne infini (pas fou de manipuler l'infini mais il peut y avoir des grandes distances)
        return self.edges.get((node1, node2), float('inf'))
    
    def exists_edge(self, node1, node2): return (node1, node2) in self.edges
    
    def from_dict(self, nodes_dict, arcs_list):
        """
            On crée le graphe à partir d'un dico : nodes_dict et d'une listes d'arêtes : arcs_list
        """
        self.nodes = []
        self.edges = {}
        self.positions = {}


        for node_id, (x, y) in nodes_dict.items():
            # Je sais pas pourquoi il faut mettre int ici 
            self.add_node(int(node_id), x, y)
    
        for node1, node2 in arcs_list:
            self.add_edge(node1, node2)
