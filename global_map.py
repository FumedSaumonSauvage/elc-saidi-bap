class global_map:
    def __init__(self, arrets, routes):
        self._arrets = arrets # [i avec i l'arret correspondant]
        self._routes = routes # {i: (j,k) with j,k in arrets}
        self._ma = {i: [0 for _ in range(len(arrets))] for i in arrets}
    
    # Getters et setters
    @property
    def arrets(self): return self._arrets

    @property
    def routes(self): return self._routes

    @property
    def ma(self): return self._ma

    @arrets.setter
    def arrets(self, arrets): self._arrets = arrets

    @routes.setter
    def routes(self, routes): self._routes = routes

    @ma.setter
    def ma(self, ma): self._ma = ma
    
    def creer_ma(self):
        """
            Choix d'une matrice d'adjacence pour laquelle si j,k arrets reliés par i route, alors ma\[j][k] = i et ma\[k][j] = i
        """
        for i, route in enumerate(self.routes):
            j, k = self.routes[route]
            self.ma[j][k] = i
            self.ma[k][j] = i