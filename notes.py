# Il nous faut une matrice U (temps nécesasire pour aller d'un noeud à un autre)
import numpy as np
class temp:
    def __init__(self, lignes_bus):
        """
            On crée le graphe de la ligne de bus à partir d'un dico de noeuds et d'une liste d'arêtes
        """
        self.lignes_bus = lignes_bus
        self.global_graph = None # Graphe global (tous les graphes de bus joints)
        self.matrice_U = None # Matrice U (temps nécessaire pour aller d'un noeud à un autre)
    
    def calculer_U(self, objective_node=None):
        for ligne_x, blx in self.lignes_bus.items():
            for i in blx.get_nodes():
                for ligne_y, bly in self.lignes_bus.items():
                    if blx == bly:
                        for j in bly.get_nodes():
                            if i != j:
                                # U_ij = temps de parcours entre i et j en utilisant blx
                                self.matrice_U[i][j] = blx.get_travel_time(i, j)
                    elif i != objective_node:
                        # On calcule le temps de parcours entre i et objective_node en utilisant blx
                        if objective_node in blx.get_nodes():
                            # Dans ce cas là, 