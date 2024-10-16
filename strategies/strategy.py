from abc import ABC, abstractmethod


class Strategy(ABC):
    @abstractmethod
    def resolver(estado_inicial):
        pass

    def mapa_a_estado(self, mapa):
        """
        Convierte el mapa del nivel en un estado del juego.
        """
        jugador = None
        cajas = set()
        objetivos = set()
        paredes = set()

        for y, row in enumerate(mapa):
            for x, char in enumerate(row):
                if char in ("@", "+"):
                    jugador = (x, y)
                if char in ("$", "*"):
                    cajas.add((x, y))
                if char in (".", "+", "*"):
                    objetivos.add((x, y))
                if char == "#":
                    paredes.add((x, y))

        return {
            "jugador": jugador,
            "cajas": cajas,
            "objetivos": objetivos,
            "paredes": paredes,
        }
