# Classe singleton qui ne sert qu'à générer des identifiants uniques

class IdCooker:
    _instance = None
    _counter = 0

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(IdCooker, cls).__new__(cls)
        return cls._instance

    def generate_id(self):
        self._counter += 1
        return self._counter
