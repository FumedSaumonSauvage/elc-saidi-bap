import math
import numpy as np
from mod.idcooker import IdCooker

class BusGraph:
    # Classe qui décrit un graphe pour un bus en particulier
    # L'ensemble des graphes des lignes (joints) forme le graphe global

    def __init__(self):
        """
            Initialise un graphe pour ce bus en particulier (ligne de bus)
        """
        self.id = IdCooker().generate_id()
        self.noeuds = {}  # id: (x, y)
        self.arcs = []  # (id_noeud1, id_noeud2)
        couleur = np.random.randint(0, 256, size=3) # Couleur aleatoire
        self.color = "#{:02x}{:02x}{:02x}".format(*couleur)
        print(f"DEBUG: BusGraph {self.id} creee avec couleur {self.color}")
    
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

    def get_edges(self): return self.arcs
    
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
    
    def to_dict(self):
        """
            Retourne le graphe de la ligne de bus sous forme de dictionnaire
        """
        return {
            "noeuds": self.noeuds,
            "arcs": self.arcs
        }


class GlobalGraph:
    # Classe qui décrit le graphe global "vierge" (sans les lignes de bus)
    # On peut donc considérer que c'est un graphe non orienté.

    def __init__(self, nodes = None, arcs = None):
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
        Cree le graphe global à partir d'un dictionnaire contenant les noeuds et les arcs
        """
        self.nodes = graph_dict["noeuds"]
        self.arcs = graph_dict["arcs"]

    def are_arcs_contingent(self, arc1, arc2):
        """
            Vérifie si deux arcs sont contigus (ie : ils partagent un nœud en commun)
        """
        return arc1[0] == arc2[0] or arc1[0] == arc2[1] or arc1[1] == arc2[0] or arc1[1] == arc2[1]
    
   

