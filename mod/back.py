# Backend, fichier principal de logique

import numpy as np
import tkinter.messagebox as tkm
from tkinter import StringVar
from tkinter.filedialog import asksaveasfile, askopenfile
import math
import json
from mod.optimizer import optimizer
from mod.graph import BusGraph, GlobalGraph

class LogiqueMetier:
    def __init__(self, canvas):
        self.canvas = canvas
        self.noeuds = {}  # id: (x, y)
        self.arcs = []  # (id_noeud1, id_noeud2, distance)
        self.debut_arc = None  # Id nœud de départ
        self.arc_temporaire = None  # Id arc temp
        self.mode = "noeud"
        self.nombre_colonies = None # PLus tard, devient un objet stringvar

    # Des ptits getter-setter pour Brams <3
    def set_mode_noeud(self):
        self.mode = "noeud"

    def set_mode_arc(self):
        self.mode = "arc"

    def setStringVar(self, objet):
        self.nombre_colonies = objet

    def is_mode_arc(self):
        return self.mode == "arc"
    
    def is_mode_noeud(self):
        return self.mode == "noeud"

    def clic_canvas(self, event):
        if self.is_mode_arc():
            self.dessiner_arc(event)
        elif self.is_mode_noeud():
            self.ajouter_noeud(event)
        else:
            print("UB clic canvas")


    def ajouter_noeud(self, event, taille_noeud=10):
        if self.mode == "noeud":
            x, y = event.x, event.y
            id_noeud = self.canvas.create_oval(x - taille_noeud, y - taille_noeud, x + taille_noeud, y + taille_noeud, fill="blue")
            self.noeuds[id_noeud] = (x, y)
        else:
            print("UB ajout noeud")
    
    def dessiner_arc(self, event):
        if self.mode == "arc":
            if self.debut_arc is None:
                x, y = event.x, event.y
                id_noeud = self.trouver_noeud_plus_proche(x, y)
                if id_noeud is not None:
                    self.debut_arc = id_noeud
                    self.arc_temporaire = self.canvas.create_line(self.noeuds[id_noeud][0], self.noeuds[id_noeud][1], x, y, fill="red", width=2, tags="arc")
            else:
                x, y = event.x, event.y
                id_noeud = self.trouver_noeud_plus_proche(x, y)
                if id_noeud is not None and id_noeud != self.debut_arc:
                    self.arcs.append((self.debut_arc, id_noeud, math.sqrt((x - self.noeuds[self.debut_arc][0])**2 + (y - self.noeuds[self.debut_arc][1])**2)))
                    self.debut_arc = None
                    self.canvas.delete(self.arc_temporaire)
                    self.afficher_arcs()
        else:
            print("UB dessin arc")


    def trouver_noeud_plus_proche(self, x, y):
        distance_min = float('inf')
        noeud_plus_proche = None
        for id_noeud, (x_noeud, y_noeud) in self.noeuds.items():
            distance = math.sqrt((x - x_noeud)**2 + (y - y_noeud)**2)
            if distance < distance_min:
                distance_min = distance
                noeud_plus_proche = id_noeud
        return noeud_plus_proche
    

    def afficher_arcs(self):
        # On vire les arcs d'avant au cas ou
        for arc_id in self.canvas.find_withtag("arc"):  # On tag les arcs (voir juste apres) pour ne pas effacer les noeuds
            self.canvas.delete(arc_id)

        print(self.noeuds)
        print(self.arcs)

        for noeud1, noeud2, _ in self.arcs:
            x1, y1 = self.noeuds[noeud1]
            x2, y2 = self.noeuds[noeud2]
            self.canvas.create_line(x1, y1, x2, y2, fill="black", width=2, tags="arc")

    def afficher_noeuds(self, taille_noeud=10):
        for noeud_id, (x, y) in self.noeuds.items():
            self.canvas.create_oval(x - taille_noeud, y - taille_noeud, x + taille_noeud, y + taille_noeud, fill="blue")


    def sauvegarder(self):
        # On pop une fenetre pour savoir ou enregistrer le fichier
        fichier = asksaveasfile(mode='w', defaultextension=".json")
        if fichier is None:
            return
        graphe = {
            "noeuds": {id_noeud: (x, y) for id_noeud, (x, y) in self.noeuds.items()},
            "arcs": self.arcs
        }
        json.dump(graphe, fichier, indent=4)
        fichier.close()
        tkm.showinfo(message="Graphe sauvegardé :)")

    def charger_graphe(self):
        # Chargement du graphe depuis un json (comme généré pendant la sauvearde)
        fichier = askopenfile(mode='r')
        if fichier is None:
            return
        graphe = json.load(fichier)
        self.noeuds = {int(id_noeud): (x, y) for id_noeud, (x, y) in graphe["noeuds"].items()}
        self.arcs = [tuple(arc) for arc in graphe["arcs"]]
        self.afficher_noeuds()
        self.afficher_arcs()
        fichier.close()


    def effacer_graphe(self):
        self.canvas.delete("all")
        self.noeuds.clear()
        self.arcs.clear()

    def afficher_ligne_bus(self, graphe_ligne, couleur, offset = 0):
        # Affiche une ligne de bus sur le canvas
        # Si la ligne de bus est seule sur le canvas, on remplace l'arête par une arête de couleur
        # Sinon, on ajoute une arête de couleur, parallèle aux autres (si plusieurs lignes passent sur une même arête, on aimerait les distinguer)
        
        for noeud1, noeud2, _ in graphe_ligne.arcs:
            x1, y1 = self.noeuds[noeud1]
            x2, y2 = self.noeuds[noeud2]
            self.canvas.create_line(x1, y1+offset, x2, y2+offset, fill=couleur, width=2)

    def afficher_tous_bus(self):
        # Affiche toutes les lignes de bus sur le canvas, pour chaque ligne de bus une couleur différente
        opti = optimizer()
        lignes_bus = opti.get_all_lignes_bus()
        for i, ligne in lignes_bus.items():
            self.afficher_ligne_bus(ligne, ligne.color, i*2)

    def afficher_legende(self, couleurs, lignes):
        # Légende le canvas, entre la couleur des lignes de bus et le numéro de la ligne
        # couleurs et lignes sont des tableaux, où couleurs[i] est la couleur de la ligne i, et lignes[i] est le numéro de la ligne i
        pos_legende = (max([x for x, y in self.noeuds.values()]) + 50, max([y for x, y in self.noeuds.values()]) - 50)
        for i in range(len(couleurs)):
            self.canvas.create_line(pos_legende[0], pos_legende[1] + i*20, pos_legende[0] + 20, pos_legende[1] + i*20, fill=couleurs[i], width=2)
            self.canvas.create_text(pos_legende[0] + 30, pos_legende[1] + i*20, text="Ligne " + str(lignes[i]), anchor="w")

    def verifier_graphe(self): # TODO : terminer la dfs
        # verifie si le graphe est bien connexe
        
        nodes_cp = self.noeuds.copy()
        arcs_cp = self.arcs.copy()
        

    def run_optimisation(self, debug = True):
        # Lance l'optimisation lorsqu'on appuie sur le bouton OK
        
        # On vérifie qu'on a >0 colonies, et que le graphe est bien en un seul morceau
        # attention, nombre_colonies est un stringvar!

        if int(self.nombre_colonies.get()) <= 0:
            tkm.showerror("Erreur", "Nombre de colonies invalide")
            return
        


        if debug: # Méthode d'optimisation: le hasard. On pose 3 lignes de bus dans le pif le plus total, juste pour voir si l'IG fonctionne.
            print("DEBUG: nombre de colonies:", self.nombre_colonies.get())
            
            # Creation du graphe global
            global_graph = GlobalGraph()
            graphe_dict = {
                "noeuds": {id_noeud: (x, y) for id_noeud, (x, y) in self.noeuds.items()},
                "arcs": self.arcs
            }
            global_graph.from_dict(graphe_dict)

            # Creation d'une ligne de bus juste pour tester
            ligne_bus = BusGraph()
            noeud1 = list(self.noeuds.keys())[0]
            noeud2 = list(self.noeuds.keys())[1]
            ligne_bus.add_node(noeud1, self.noeuds[noeud1][0], self.noeuds[noeud1][1])
            ligne_bus.add_node(noeud2, self.noeuds[noeud2][0], self.noeuds[noeud2][1])
            ligne_bus.add_edge(noeud1, noeud2)

            ligne_bus_2 = BusGraph()
            noeud3 = list(self.noeuds.keys())[0]
            noeud4 = list(self.noeuds.keys())[1]
            noeud5 = list(self.noeuds.keys())[2]
            ligne_bus_2.add_node(noeud3, self.noeuds[noeud3][0], self.noeuds[noeud3][1])
            ligne_bus_2.add_node(noeud4, self.noeuds[noeud4][0], self.noeuds[noeud4][1])
            ligne_bus_2.add_node(noeud5, self.noeuds[noeud5][0], self.noeuds[noeud5][1])
            ligne_bus_2.add_edge(noeud3, noeud4)
            ligne_bus_2.add_edge(noeud4, noeud5)
            
            # affichage
            self.afficher_ligne_bus(ligne_bus, ligne_bus.color, 4)
            self.afficher_ligne_bus(ligne_bus_2, ligne_bus_2.color, 2)
            self.afficher_legende([ligne_bus.color, ligne_bus_2.color], [1, 2])

        pass

