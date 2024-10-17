

class Strategy():


    def __init__(self, mapa):
        # Estado inicial del juego: posiciones del jugador y cajas
        self.estado_inicial = self.mapa_a_estados(mapa)

        # Métricas adicionales
        self.nodos_generados = 0
        self.nodos_abiertos = 0
        self.nodos_cerrados = 0
        self.profundidad_maxima = 0
    
    def resolver(estado_inicial):
        pass

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
                        movimientos.append((nuevo_estado, direccion))
                        self.nodos_generados += 1  # Incrementar el contador de nodos generados
                else:
                    # Si no hay caja, simplemente mueve el jugador
                    nuevo_estado = {
                        "jugador": nuevo_jugador,
                        "cajas": estado["cajas"],
                        "objetivos": estado["objetivos"],
                        "paredes": estado["paredes"],
                    }
                    movimientos.append((nuevo_estado, direccion))
                    self.nodos_generados += 1  # Incrementar el contador de nodos generados

        return movimientos

    def preparar_respuesta(self, camino):
        """
        Prepara la respuesta final con el camino y las métricas.
        """
        return {
            "camino": camino,
            "nodos_generados": self.nodos_generados,
            "nodos_abiertos": self.nodos_abiertos,
            "nodos_cerrados": self.nodos_cerrados,
            "profundidad_maxima": self.profundidad_maxima,
        }

    def mapa_a_estados(self, mapa):
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
