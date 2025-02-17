class lignes_bus:
    def __init__(self, id, arrets):
        self._id = id
        self._arrets = arrets

    # Getters et setters
    @property
    def id(self): return self._id

    @property
    def arrets(self): return self._arrets

    @id.setter
    def id(self, id): self._id = id

    @arrets.setter
    def arrets(self, arrets): self._arrets = arrets