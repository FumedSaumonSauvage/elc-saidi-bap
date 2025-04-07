# Fichier pilote de l'interface

import matplotlib.pyplot as plt
import tkinter as tk
import numpy as np

class InterfaceUtilisateur:
    def __init__(self, app):
        master = app.root
        self.master = master
        self.app = app
        master.geometry("1400x900")

        # Frame principal pour le canvas et les paramètres avec padding
        main_frame = tk.Frame(master, padx=10, pady=10)
        main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Zone dessin (à gauche)
        self.canvas = tk.Canvas(main_frame, width=600, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # Volet de paramètres (à droite)
        self.param_frame = tk.Frame(main_frame)
        self.param_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Barre d'outils (en bas) avec padding
        self.toolbar_frame = tk.Frame(master, padx=10, pady=10)
        self.toolbar_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Contenu de la barre d'outils
        self.bouton_noeud = tk.Button(self.toolbar_frame, text="Dessiner nœud", command=self.set_mode_noeud)
        self.bouton_noeud.pack(side=tk.LEFT)

        self.bouton_arc = tk.Button(self.toolbar_frame, text="Dessiner arc", command=self.set_mode_arc)
        self.bouton_arc.pack(side=tk.LEFT)

        self.bouton_effacer = tk.Button(self.toolbar_frame, text="Effacer", command=self.effacer_graphe)
        self.bouton_effacer.pack(side=tk.LEFT)

        self.bouton_sauvegarder = tk.Button(self.toolbar_frame, text="Sauvegarder", command=self.sauvegarder)
        self.bouton_sauvegarder.pack(side=tk.LEFT)

        self.bouton_charger = tk.Button(self.toolbar_frame, text="Charger", command=self.charger_graphe)
        self.bouton_charger.pack(side=tk.LEFT)

        self.bouton_ajouter_colonies = tk.Button(self.toolbar_frame, text="OK", command=self.start_optimisation)
        self.bouton_ajouter_colonies.pack(side=tk.RIGHT)

        nombre_colonies = tk.StringVar()
        self.entry_nombre = tk.Entry(self.toolbar_frame, width=5, textvariable=nombre_colonies)
        self.entry_nombre.pack(side=tk.RIGHT)
        self.nombre_colonies_var = nombre_colonies 
        app.passer_ref_stringvar(nombre_colonies) 

        self.label_nombre = tk.Label(self.toolbar_frame, text="Nb. colonies:")
        self.label_nombre.pack(side=tk.RIGHT)

        # Contenu de la zone de paramètres
        params = {
            "alpha": (0.1, 5.0, 0.1),
            "beta": (0.1, 5.0, 0.1),
            "tau": (0.1, 10.0, 0.1),
            "rho": (0.01, 1.0, 0.01),
            "q0": (0.0, 1.0, 0.01),
            "nb_fourmis": (1, 100, 1),
            "nb_iterations": (1, 1000, 1)
        }

        self.sliders = {}
        for param, (min_val, max_val, step) in params.items():
            frame = tk.Frame(self.param_frame)
            frame.pack(fill=tk.X, pady=5)

            label = tk.Label(frame, text=param, width=12, anchor="w")
            label.pack(side=tk.LEFT)

            slider = tk.Scale(
            frame, from_=min_val, to=max_val, resolution=step,
            orient=tk.HORIZONTAL, length=200
            )
            slider.pack(side=tk.RIGHT, fill=tk.X, expand=1)
            self.sliders[param] = slider

        # Liaison du clic du canvas à la logique métier
        self.canvas.bind("<Button-1>", self.clic_canvas)

    def set_mode_noeud(self):
        if hasattr(self.app, 'logique'):
            self.app.logique.set_mode_noeud()
        else:
            print("logique non initialisée dans main")

    def set_mode_arc(self):
        if hasattr(self.app, 'logique'):
            self.app.logique.set_mode_arc()
        else:
            print("logique non initialisée dans main")

    def clic_canvas(self, event):
        if hasattr(self.app, 'logique'):
            self.app.logique.clic_canvas(event)
        else:
            print("logique non initialisée dans main")

    def sauvegarder(self):
        if hasattr(self.app, 'logique'):
            self.app.logique.sauvegarder()
        else:
            print("logique non initialisée dans main")

    def charger_graphe(self):
        if hasattr(self.app, 'logique'):
            self.app.logique.charger_graphe()
        else:
            print("logique non initialisée dans main")

    def effacer_graphe(self):
        if hasattr(self.app, 'logique'):
            self.app.logique.effacer_graphe()
        else:
            print("logique non initialisée dans main")

    def start_optimisation(self):
        if hasattr(self.app, 'logique'):
            params = {
                param: slider.get() for param, slider in self.sliders.items()
            }
            nb_colonies = int(self.nombre_colonies_var.get())
            self.app.logique.run_optimisation(
                nb_colonies=nb_colonies,
                alpha=params.get("alpha"),
                beta=params.get("beta"),
                tau=params.get("tau"),
                rho=params.get("rho"),
                q0=params.get("q0"),
                nb_fourmis=params.get("nb_fourmis"),
                nb_iterations=params.get("nb_iterations")
            )
        else:
            print("logique non initialisée dans main")