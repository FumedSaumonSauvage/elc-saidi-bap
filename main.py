import tkinter as tk
from mod.interface import InterfaceUtilisateur
from mod.back import LogiqueMetier

class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Projet BAP")

        try:
            self.root.iconbitmap("assets/bus.ico")
        except:
            print("Impossible de charger l'icone")

        self.interface = InterfaceUtilisateur(self)
        self.logique = LogiqueMetier(self.interface.canvas)
        self.logique.setStringVar(self.stringvar) # Méthode dégueulasse de la stringvar

        self.interface.bouton_sauvegarder.config(command=self.logique.sauvegarder)
        self.interface.bouton_noeud.config(command=self.logique.set_mode_noeud)
        self.interface.bouton_arc.config(command=self.logique.set_mode_arc)
        self.interface.bouton_effacer.config(command=self.logique.effacer_graphe)
        self.interface.bouton_charger.config(command=self.logique.charger_graphe)
        self.interface.bouton_ajouter_colonies.config(command=self.logique.run_optimisation)

        self.interface.canvas.bind("<Button-1>", self.logique.clic_canvas)
        

        self.root.mainloop()

    def passer_ref_stringvar(self, objet): # Méthode quick & dirty pour passer l'objet stringvar vers le backend
        self.stringvar = objet


if __name__ == "__main__":
    app = Application()
