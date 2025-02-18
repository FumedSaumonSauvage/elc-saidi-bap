# Fichier pilote de l'interface

import matplotlib.pyplot as plt
import tkinter as tk
import numpy as np

class InterfaceUtilisateur:
    def __init__(self, master):
        self.master = master
        master.geometry("900x700")

        # Zone dessin
        self.canvas = tk.Canvas(master, width=600, height=400, bg="white")
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Toolbar
        self.toolbar_frame = tk.Frame(master)
        self.toolbar_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.bouton_noeud = tk.Button(self.toolbar_frame, text="Dessiner nœud")
        self.bouton_noeud.pack(side=tk.LEFT)

        self.bouton_arc = tk.Button(self.toolbar_frame, text="Dessiner arc")
        self.bouton_arc.pack(side=tk.LEFT)

        self.bouton_effacer = tk.Button(self.toolbar_frame, text="Effacer")
        self.bouton_effacer.pack(side=tk.LEFT)

        self.bouton_sauvegarder = tk.Button(self.toolbar_frame, text="Sauvegarder")
        self.bouton_sauvegarder.pack(side=tk.LEFT)

        self.bouton_charger = tk.Button(self.toolbar_frame, text="Charger")
        self.bouton_charger.pack(side=tk.LEFT)