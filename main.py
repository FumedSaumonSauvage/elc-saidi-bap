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

        self.interface = InterfaceUtilisateur(self.root)
        self.logique = LogiqueMetier(self.interface.canvas)

        self.interface.bouton_sauvegarder.config(command=self.logique.sauvegarder)
        self.interface.bouton_noeud.config(command=self.logique.set_mode_noeud)
        self.interface.bouton_arc.config(command=self.logique.set_mode_arc)
        self.interface.bouton_effacer.config(command=self.logique.effacer_graphe)
        self.interface.bouton_charger.config(command=self.logique.charger_graphe)

        self.interface.canvas.bind("<Button-1>", self.logique.clic_canvas)
        

        self.root.mainloop()

if __name__ == "__main__":
    app = Application()
