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
    
    def add_edge(self, node1, node2, poids):
        """
            Ajoute une arête entre deux nœuds qui existent déjà
        """
        # On vérifie qu'il existe bien les deux noeuds ainsi que l'arête qui les relie
        if not self.exists_edge(node1, node2) and node1 in self.noeuds and node2 in self.noeuds:
            self.arcs.append((node1, node2, poids))
            self.arcs.append((node2, node1, poids)) 
        else:
            print(f"DEBUG: Impossible d'ajouter l'arête entre {node1} et {node2} car elle existe déjà ou les noeuds n'existent pas")

    def get_id(self): return self.id

    def get_color(self): return self.color

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
    
    def expansion(self, global_graph):
        """
            Pour chaque noeud de la ligne de bus, on étend la ligne à ses voisins en regardant le graphe global
            global_graph: GlobalGraph()
        """
        for node in self.noeuds:
            for neighbor in global_graph.nodes:
                if global_graph.exists_edge(node, neighbor):
                    self.add_node(neighbor, *global_graph.nodes[neighbor])
                    self.add_edge(node, neighbor)


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
        return any(arc[0] == node1 and arc[1] == node2 for arc in self.arcs) or any(arc[0] == node2 and arc[1] == node1 for arc in self.arcs)
    
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
    
    def get_2_random_nodes_init(self):
        """
        Renvoie 2 noeuds au hasard, parcourus par une arête.
        Utilisé dans la création de lignes de bus lors de l'optimisation.
        """
        arc = self.arcs[np.random.randint(0, len(self.arcs))]
        return arc[0], arc[1], arc[2]

    def get_random_node(self):
        """
        Renvoie un noeud au hasard
        """
        return np.random.choice(list(self.nodes.keys()))
    
    def get_nodes(self):
        """
        Renvoie les noeuds du graphe
        """
        return self.nodes
