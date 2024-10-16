from collections import deque
from strategies.strategy import Strategy


class IDDFSStrategy(Strategy):
    def __init__(self, mapa):
        # Estado inicial del juego: posiciones del jugador y cajas
        self.estado_inicial = super().mapa_a_estado(mapa)

    def es_estado_objetivo(self, estado):
        """
        Verifica si el estado es objetivo, es decir, si todas las cajas están en los objetivos.
        """
        return estado["cajas"] == estado["objetivos"]

    def generar_movimientos(self, estado):
        """
        Genera movimientos válidos para el jugador y las cajas en el estado actual.
        """
        movimientos = []
        jugador_x, jugador_y = estado["jugador"]

        # Movimientos posibles y sus correspondientes notaciones LURD
        desplazamientos = {
            "U": (0, -1),  # Arriba
            "D": (0, 1),  # Abajo
            "L": (-1, 0),  # Izquierda
            "R": (1, 0),  # Derecha
        }

        for direccion, (dx, dy) in desplazamientos.items():
            nuevo_jugador = (jugador_x + dx, jugador_y + dy)

            # Verifica si el movimiento es válido (no se sale del tablero ni choca con una pared)
            if nuevo_jugador not in estado["paredes"]:
                # Si hay una caja en la posición, verifica si se puede empujar
                if nuevo_jugador in estado["cajas"]:
                    nueva_caja = (nuevo_jugador[0] + dx, nuevo_jugador[1] + dy)

                    # La nueva posición de la caja debe estar vacía y no ser una pared o caja
                    if (
                        nueva_caja not in estado["paredes"]
                        and nueva_caja not in estado["cajas"]
                    ):
                        nuevo_estado = {
                            "jugador": nuevo_jugador,
                            "cajas": estado["cajas"] - {nuevo_jugador} | {nueva_caja},
                            "objetivos": estado["objetivos"],
                            "paredes": estado["paredes"],
                        }
                        movimientos.append(
                            (nuevo_estado, direccion)
                        )  # Agregar dirección al movimiento
                else:
                    # Si no hay caja, simplemente mueve el jugador
                    nuevo_estado = {
                        "jugador": nuevo_jugador,
                        "cajas": estado["cajas"],
                        "objetivos": estado["objetivos"],
                        "paredes": estado["paredes"],
                    }
                    movimientos.append(
                        (nuevo_estado, direccion)
                    )  # Agregar dirección al movimiento

        return movimientos

    def profundidad_limitada(self, estado, camino, limite, visited):
        """
        Realiza búsqueda en profundidad hasta un límite de profundidad.
        """
        # Verifica si el estado actual es objetivo
        if self.es_estado_objetivo(estado):
            return camino

        # Si el límite es cero, no profundizamos más
        if limite <= 0:
            return None

        # Marca este estado como visitado
        estado_clave = (estado["jugador"], frozenset(estado["cajas"]))
        visited.add(estado_clave)

        for nuevo_estado, direccion in self.generar_movimientos(estado):
            nuevo_estado_clave = (
                nuevo_estado["jugador"],
                frozenset(nuevo_estado["cajas"]),
            )

            # Si el estado no ha sido visitado en este nivel de profundidad
            if nuevo_estado_clave not in visited:
                resultado = self.profundidad_limitada(
                    nuevo_estado, camino + direccion, limite - 1, visited
                )
                if resultado is not None:
                    return resultado

        return None

    def resolver(self):
        """
        Ejecuta la búsqueda en profundidad iterativa para encontrar la solución.
        """
        limite = 0  # Empieza con profundidad 0
        while True:
            # Utiliza búsqueda en profundidad hasta el límite actual
            visited = set()  # Reinicia el conjunto de visitados en cada iteración
            resultado = self.profundidad_limitada(
                self.estado_inicial, "", limite, visited
            )

            # Si encuentra la solución, la devuelve
            if resultado is not None:
                return resultado

            # Aumenta el límite y sigue buscando
            limite += 1
