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
        self.arcs = []  # (id_noeud1, id_noeud2, temps_de_parcours)
        color = np.random.randint(0, 256, size=3) # Couleur aleatoire
        self.couleur = "#{:02x}{:02x}{:02x}".format(*color)
        print(f"DEBUG: BusGraph {self.id} crée avec couleur {self.couleur}")
    
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
            self.add_arc(node1, node2, tps_parcours)
            self.add_arc(node2, node1, tps_parcours) 
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

    ##### Modifications et refonte bien propre #####

    def add_node(self, node_id, x, y): self.noeuds[node_id] = (x, y)
    
    def add_arc(self, node1, node2, poids):
        # On vérifie qu'il existe bien les deux noeuds ainsi que l'arête qui les relie
        if not self.exists_arc(node1, node2) and node1 in self.noeuds and node2 in self.noeuds:
            self.arcs.append((node1, node2, poids))
            self.arcs.append((node2, node1, poids)) 
        else:
            if node1 in self.noeuds and node2 in self.noeuds:
                print(f"DEBUG: Impossible d'ajouter l'arête entre {node1} et {node2} car elle existe déjà")
            else:
                if node1 not in self.noeuds:
                    print(f"DEBUG: Impossible d'ajouter l'arête entre {node1} et {node2} car le noeud {node1} n'existe pas")
                if node2 not in self.noeuds:
                    print(f"DEBUG: Impossible d'ajouter l'arête entre {node1} et {node2} car le noeud {node2} n'existe pas")

    def get_travel_time(self, node1, node2):
        """ Fonction qui permet de récupérer le temps de parcours entre deux noeuds d'une ligne de bus"""
        if self.exists_arc(node1, node2):
            for arc in self.arcs:
                if (arc[0] == node1 and arc[1] == node2) or (arc[0] == node2 and arc[1] == node1):
                    return arc[2]
        return None  # Si l'arête n'existe pas, on retourne None
    
    def contains_node(self, node_id): return node_id in self.noeuds
    
    def get_id(self): return self.id

    def get_color(self): return self.color

    def get_nodes(self): return self.noeuds

    def get_arcs(self): return self.arcs
    
    def exists_arc(self, node1, node2):
        return any(arc[0] == node1 and arc[1] == node2 for arc in self.arcs)

    def expansion(self, global_graph):
        """
            Étend la ligne de bus en ajoutant un seul arc par appel.
            global_graph: GlobalGraph()
        """
        visited_nodes = set(self.noeuds.keys())  # Ensemble des noeuds déjà visités

        # Parcourt les noeuds déjà visités pour trouver un voisin non visité
        for current_node in self.noeuds.keys():
            neighbors = global_graph.get_neighbors(current_node)  # Récupère les voisins du noeuds actuel dans le graphe global
            
            for neighbor in neighbors:
                # Vérifie que le voisin n'a pas été visité et qu'il existe un arc entre les deux noeuds
                if neighbor not in visited_nodes and global_graph.exists_arc(current_node, neighbor):
                    self.add_node(neighbor, *global_graph.nodes[neighbor])  # Ajoute le voisin au graphe du bus
                    self.add_arc(current_node, neighbor, global_graph.get_arc(current_node, neighbor)[2])  # Ajoute l'arc
                    return  # Arrête l'expansion après avoir ajouté un seul arc


class GlobalGraph:
    # Classe qui décrit le graphe global "vierge" (sans les lignes de bus)

    def __init__(self, nodes = None, arcs = None):
        """
            Initialise le graphe global
            nodes: format {id_noeud: (x, y)}
            arcs: format [(id_noeud1, id_noeud2, temps_parcours)] --> asymétrique
        """
        self.nodes = nodes
        self.arcs = arcs 
    
    def from_dict(self, graph_dict):
        """
        Crée le graphe global à partir d'un dictionnaire contenant les noeuds et les arcs
        """
        self.nodes = graph_dict["noeuds"]
        self.arcs = graph_dict["arcs"]

    def exists_arc(self, node1, node2):
        """
            Vérifie si une arête existe entre deux nœuds dans le graphe global (ie : il existe au moins une ligne de bus qui relie les deux noeuds)
        """
        return any(arc[0] == node1 and arc[1] == node2 for arc in self.arcs) or any(arc[0] == node2 and arc[1] == node1 for arc in self.arcs)

    def get_random_node(self):
        """
        Renvoie un noeud au hasard
        """
        return np.random.choice(list(self.nodes.keys()))
    
    def get_random_node_pair(self):
        """
        Renvoie 2 noeuds au hasard, parcourus par une arête.
        Utilisé dans la création de lignes de bus lors de l'optimisation.
        """
        arc = self.arcs[np.random.randint(0, len(self.arcs))]
        return arc[0], arc[1], arc[2] 
    
    def get_arc(self, node1, node2):
        """
        Renvoie l'arête entre deux noeuds
        """
        for arc in self.arcs:
            if (arc[0] == node1 and arc[1] == node2) or (arc[0] == node2 and arc[1] == node1):
                return arc
        return None

    def get_neighbors(self, node_id):
        """
        Renvoie les voisins d'un noeud
        """
        neighbors = []
        for arc in self.arcs:
            if arc[0] == node_id:
                neighbors.append(arc[1])
            elif arc[1] == node_id:
                neighbors.append(arc[0])
        return neighbors

    def get_nodes(self):
        """
        Renvoie les noeuds du graphe
        """
        return self.nodes
    
    def get_arcs(self):
        """
        Renvoie les arcs du graphe
        """
        return self.arcs
