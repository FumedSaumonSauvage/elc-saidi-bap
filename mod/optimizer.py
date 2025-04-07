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

    def initialiser_attributs(self, nb_lignes_bus, global_graph, nb_fourmis, nb_iterations, alpha, beta, gamma, rho, q0, tau0, conn_ig):
        """
            Initialise les attributs du problème d'optimisation
            Paramètres:
                nb_lignes_bus: le nombre de lignes de bus à créer
                global_graph: le graphe global du problème, classe GlobalGraph
                nb_fourmis: le nombre de fourmis par colonie
                nb_iterations: le nombre d'itérations de l'algorithme
                conn_ig: connexion à l'interface graphique par Logique_metier
        """

        self.nb_lignes_bus = nb_lignes_bus
        self.global_graph = global_graph
        self.nb_iterations = nb_iterations

        # Initialisation des lignes de bus:
        print(f"DEBUG: Initialisation des lignes de bus")
        self.lignes_bus = {}
        for i in range(self.nb_lignes_bus):
            self.lignes_bus[i] = BusGraph() # Pour le moment, les lignes de bus sont vides
        # Initialisation des systèmes de colonies de fourmis
        noeud_depart = self.global_graph.get_random_node()
        noeud_arrivee = self.global_graph.get_random_node()

        qte_pheromones = 1 # Quantité de phéromones à déposer par les fourmis
        
        print(f"DEBUG: Initialisation des colonies de fourmis")
        self.acs = {}
        for i in range(self.nb_lignes_bus):
            self.acs[i] = Ant_Colony(
                i, nb_fourmis, self.global_graph, noeud_depart, noeud_arrivee,
                qte_pheromones, alpha, beta, gamma, rho, q0, tau0, lignes_bus=self.lignes_bus
            )

        self.connexion_interface = conn_ig

        self.initialized = True
        print(f"DEBUG: Initialisation de l'optimizer terminée")

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
    def test_efficacite(self):
        # On veut deux choses:
        # - Pour tout couple de noeuds (arrêts) du graphe global, on veut pouvoir voyager de l'un à l'autre en prenant un (ou plusieurs) bus. Si c'est impossible (graphe disjoint), ca sert à rien de continuer
        # - On veut minimiser ce temps moyen de voyage entre deux noeuds pris au hasard
        
        if not self.test_couverture_bus_2():
            return -1
        
        total_time = 0
        num_pairs = 0

        # On parcourt tous les couples de noeuds du graphe global afin de calculer tous les temps de trajet (nécessite un graphe connexe et recouvert par les lignes de bus)
        for node1 in self.global_graph.nodes:
            for node2 in self.global_graph.nodes:
                if node1 != node2:
                    shortest_time = float('inf')
                    for ligne_id, bus_graph in self.lignes_bus.items():
                        travel_time = bus_graph.exists_path(node1, node2)
                        if travel_time != -1: # exists_path renvoie -1 si le chemin n'existe pas
                            shortest_time = min(shortest_time, travel_time) 
                    if shortest_time == float('inf'):
                        return -1  # Impossible de voyager entre deux noeuds, en théorie on a déjà vérifié ça avant
                    total_time += shortest_time
                    num_pairs += 1

        return total_time / num_pairs # utilisation tu temps de trajet moyen
    

    def test_couverture_bus(self):
        # Vérifie si tout noeud du graphe est accessible par un voyageur prenant le bus
        for node in self.global_graph.nodes: # Vérifie si chaque noeud est accessible par une ligne de bus
            if not any(bus_graph.exists_arc(node, _) for _, bus_graph in self.lignes_bus.items()):
                return False
            
        repertoire_noeuds_contact = {} # Noeud i , ligne_bus 1, ligne_bus 2
            
        for noeud in self.global_graph.nodes: # Pour chaque noeud, si plusieurs lignes passent dessus on les ajoute dans le répertoire de contact
            lignes_contenant_noeud = [
                ligne_id for ligne_id, bus_graph in self.lignes_bus.items()
                if any(bus_graph.exists_arc(noeud, _) for _ in self.global_graph.nodes)
            ]
            if len(lignes_contenant_noeud) > 1:
                repertoire_noeuds_contact[noeud] = lignes_contenant_noeud

        lignes_contact = []
        lignes_contact.append(self.lignes_bus[0])
        for ligne in self.lignes_bus:
            if ligne not in lignes_contact:
                apparitions_repertoire = [
                        noeud for noeud, lignes in repertoire_noeuds_contact.items()
                        if ligne in lignes
                    ]
                voisins = [
                    other_ligne for noeud in apparitions_repertoire
                    for other_ligne in repertoire_noeuds_contact[noeud]
                    if other_ligne != ligne and other_ligne not in voisins
                ]
                if any(voisin in lignes_contact for voisin in voisins):
                    lignes_contact.append(ligne)

        return len(lignes_contact) == len(self.lignes_bus)
                
    def test_couverture_bus_2(self):
        """
        Vérifie si chaque nœud du graphe est accessible via au moins une ligne de bus.
        Pour chaque ligne de bus, on vérifie si cette ligne couvre un ou plusieurs nœuds dans le graphe.
        Retourne True si toutes les lignes de bus recouvrent l'ensemble des nœuds, sinon False.
        """

        # Crée un ensemble pour garder trace des nœuds couverts
        noeuds_recouverts = set()

        # Pour chaque ligne de bus
        for bus_graph in self.lignes_bus.values():
            # On parcourt les nœuds de la ligne de bus et on les ajoute à l'ensemble des nœuds recouverts
            for noeud in bus_graph.noeuds:
                noeuds_recouverts.add(noeud)

        # On vérifie si l'ensemble des nœuds recouverts est égal à l'ensemble des nœuds du graphe global
        return noeuds_recouverts == set(self.global_graph.nodes)


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

        print(f"DEBUG: Lancement de l'optimisation...")

        print(f"DEBUG: Démarrage des lignes de bus")
        # Attribution de 2 neods pour chaque ligne de bus
        for i in range(self.nb_lignes_bus):
            point1, point2, poids= self.global_graph.get_random_node_pair()
            self.lignes_bus[i].add_node(point1, *self.global_graph.nodes[point1])
            self.lignes_bus[i].add_node(point2, *self.global_graph.nodes[point2])
            self.lignes_bus[i].add_arc(point1, point2, poids)
        
        print(f"DEBUG: Expansion des lignes de bus...")
        # Expansion des lignes de bus
        while not self.test_couverture_bus_2():
            for i in range(self.nb_lignes_bus):
                self.lignes_bus[i].expansion(self.global_graph)
        self.maj_interface()
        self.initialiser_interface()

        print(f"DEBUG: Lancement itération")
        for iteration in range(self.nb_iterations):
            print(f"Iteration {iteration+1}/{self.nb_iterations}")
            for i in range(self.nb_lignes_bus):
                for j in range(self.acs[i].nb_fourmis):
                    self.acs[i].fourmis[j].choix_noeud()
                    self.acs[i].fourmis[j].deplacement()
                self.maj_interface()

        pass

    def maj_interface(self):
        # Mise à jour de l'interface: on affiche sur chaque arc quelle ligne de bus passe par là
        # On efface les anciennes lignes de bus
        self.connexion_interface.effacer_lignes_bus()

        # On affiche les nouvelles lignes de bus
        offset = 0
        couleurs = []
        id_lignes = []
        for id, ligne_bus in self.lignes_bus.items():
            couleurs.append(ligne_bus.couleur)
            id_lignes.append(ligne_bus.id)
            offset += 2
            self.connexion_interface.afficher_ligne_bus(ligne_bus, ligne_bus.couleur, offset)
    
    def initialiser_interface(self):
        # Sert juste à n'afficher la légende qu'une fois
        couleurs = []
        id_lignes = []
        for id, ligne_bus in self.lignes_bus.items():
            couleurs.append(ligne_bus.couleur)
            id_lignes.append(ligne_bus.id)

        self.connexion_interface.afficher_legende(couleurs, id_lignes)