# Backend, fichier principale- de logique

import numpy as np
import tkinter.messagebox as tkm
from tkinter.filedialog import asksaveasfile, askopenfile
import math
import json

class LogiqueMetier:
    def __init__(self, canvas):
        self.canvas = canvas
        self.noeuds = {}  # id: (x, y)
        self.arcs = []  # (id_noeud1, id_noeud2)
        self.debut_arc = None  # Id nœud de départ
        self.arc_temporaire = None  # Id arc temp
        self.mode = "noeud"

    # Des ptits getter-setter pour Brams <3
    def set_mode_noeud(self):
        self.mode = "noeud"

    def set_mode_arc(self):
        self.mode = "arc"

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


    def ajouter_noeud(self, event):
        if self.mode == "noeud":
            x, y = event.x, event.y
            id_noeud = self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="blue")
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
                    self.arcs.append((self.debut_arc, id_noeud))
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

        for noeud1, noeud2 in self.arcs:
            x1, y1 = self.noeuds[noeud1]
            x2, y2 = self.noeuds[noeud2]
            self.canvas.create_line(x1, y1, x2, y2, fill="black", width=2, tags="arc")

    def afficher_noeuds(self):
        for noeud_id, (x, y) in self.noeuds.items():
            self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="blue")


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
        self.noeuds = graphe["noeuds"]
        self.arcs = graphe["arcs"]
        self.afficher_noeuds()
        self.afficher_arcs() # TODO: voir pourquoi c'est pété
        fichier.close()


    def effacer_graphe  (self):
        self.canvas.delete("all")
        self.noeuds.clear()
        self.arcs.clear()