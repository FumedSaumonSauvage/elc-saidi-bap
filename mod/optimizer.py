# Classe qui gère toute l'organisation du problème d'optimisation. C'est un singleton, et regroupe les différentes classes qui composent le problème.
import numpy as np
from mod.graph import GlobalGraph, BusGraph
from mod.acs import Ant_Colony, Ant

class optimizer:
    _instance = None

    def __new__(cls, *args, **kwargs): # Spécifique au design pattern singleton, si tu comprends pas c'est pas grave
        if cls._instance is None:
            cls._instance = super(optimizer, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        
        if not hasattr(self, 'initialized'):
            self.initialized = False

    def initialiser_attributs(self, nb_lignes_bus, global_graph, nb_fourmis, nb_iterations, alpha, beta, rho, q0, tau0, conn_ig):
        """
            Initialise les attributs du problème d'optimisation
            Paramètres:
                nb_lignes_bus: le nombre de lignes de bus à créer
                global_graph: le graphe global du problème
                nb_fourmis: le nombre de fourmis par colonie
                nb_iterations: le nombre d'itérations de l'algorithme
                conn_ig: connexion à l'interface graphique par Logique_metier
        """

        self.nb_lignes_bus = nb_lignes_bus
        self.global_graph = global_graph

        # Initialisation des lignes de bus:
        self.lignes_bus = {}
        for i in range(self.nb_lignes_bus):
            self.lignes_bus[i] = BusGraph() # Pour le moment, les lignes de bus sont vides

        # Initialisation des systèmes de colonies de fourmis
        self.acs = {}
        for i in range(self.nb_lignes_bus):
            self.acs[i] = Ant_Colony(self.global_graph, i, alpha, beta, rho, q0, tau0)

        connexion_interface = conn_ig

        self.initialized = True

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


    # Test de l'efficacité de la solution du problème
    def test_efficacite():
        # On veut deux choses:
        # - Pour tout couple de noeuds (arrêts) du graphe global, on veut pouvoir voyager de l'un à l'autre en prenant un (ou plusieurs) bus. Si c'est impossible (graphe disjoint), ca sert à rien de continuer
        # - On veut minimiser ce temps moyen de voyage entre deux noeuds pris au hasard
        pass

    def run(self):
        """
            Lance l'optimisation.
            Devrait ressembler à qqch commme:

            Créer des lignes de bus au hasard (taille 1)

            Pour chaque itération:
                Pour chaque colonie:
                    Pour chaque fourmi:
                        fourmi.choix_noeud()
                        fourmi.deposer_pheromones()
                    colonie.update_pheromones()
                    colonie.update_visites()
                    màj_interface()
        """
        pass



