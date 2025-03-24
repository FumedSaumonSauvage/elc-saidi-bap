# Classe qui gère toute l'organisation du problème d'optimisation. C'est un singleton, et regroupe les différentes classes qui composent le problème.

from mod.graph import GlobalGraph, BusGraph
from mod.acs import AntColonySystem

class optimizer:
    _instance = None

    def __new__(cls, *args, **kwargs): # Spécifique au design pattern singleton, si tu comprends pas c'est pas grave
        if cls._instance is None:
            cls._instance = super(optimizer, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, nb_lignes_bus = None, global_graph_dict = None, nb_fourmis = 10, nb_iterations = 100, alpha=1.0, beta=2.0, rho=0.1, q0=0.9, tau0=None):
        # TODO: voir ce qu'on fait du param nb_fourmis
        
        if not hasattr(self, 'initialized'):
            self.initialized = True

            # Initialisation des attributs
            if nb_lignes_bus is not None:
                self.nb_lignes_bus = nb_lignes_bus
            else:
                self.nb_lignes_bus = 0
            
            self.global_graph = GlobalGraph()
            if global_graph_dict is not None:
                self.global_graph.from_dict(global_graph_dict)

            # Initialisation des lignes de bus:
            self.lignes_bus = {}
            for i in range(self.nb_lignes_bus):
                self.lignes_bus[i] = BusGraph() # Pour le moment, les lignes de bus sont vides

            # Initialisation des systèmes de colonies de fourmis
            self.acs = {}
            for i in range(self.nb_lignes_bus):
                self.acs[i] = AntColonySystem(self.global_graph, i, alpha, beta, rho, q0, tau0)
            

    def add_ligne_bus(self, id, arrets):
        """
            Ajoute une ligne de bus au problème
        """
        self.lignes_bus[id] = BusGraph(id, arrets)

    def get_ligne_bus(self, id):
        """
            Retourne la ligne de bus id
        """
        return self.lignes_bus[id]

    def get_all_lignes_bus(self):
        """
            Retourne toutes les lignes de bus
        """
        return self.lignes_bus

    def charger_graphe(self, graph_dict):
        """
            Charge le graphe global à partir d'un dictionnaire
        """
        self.global_graph.from_dict(graph_dict)

    # Test de l'efficacité de la solution du problème
    def test_efficacite():
        # On veut deux choses:
        # - Pour tout couple de noeuds (arrêts) du graphe global, on veut pouvoir voyager de l'un à l'autre en prenant un (ou plusieurs) bus. Si c'est impossible (graphe disjoint), ca sert à rien de continuer
        # - On veut minimiser ce temps moyen de voyage entre deux noeuds pris au hasard
        pass



