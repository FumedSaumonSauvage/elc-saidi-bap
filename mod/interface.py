# Fichier pilote de l'interface

import matplotlib.pyplot as plt
import tkinter as tk
import numpy as np

class InterfaceUtilisateur:
    def __init__(self, app):
        master = app.root
        self.master = master
        master.geometry("1000x700")

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

        self.bouton_ajouter_colonies = tk.Button(self.toolbar_frame, text="OK")
        self.bouton_ajouter_colonies.pack(side=tk.RIGHT)

        nombre_colonies = tk.StringVar()
        self.entry_nombre = tk.Entry(self.toolbar_frame, width=5, textvariable=nombre_colonies)
        self.entry_nombre.pack(side=tk.RIGHT)
        app.passer_ref_stringvar(nombre_colonies) # Envoie l'objet au master, qui transmet au back

        self.label_nombre = tk.Label(self.toolbar_frame, text="Nb. colonies:")
        self.label_nombre.pack(side=tk.RIGHT)

        
