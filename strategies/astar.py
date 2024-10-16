from collections import deque
import heapq
from strategies.strategy import Strategy


class AStarStrategy(Strategy):
    def __init__(self, mapa):
        # Estado inicial del juego: posiciones del jugador y cajas
        self.estado_inicial = super().mapa_a_estado(mapa)

    def es_estado_objetivo(self, estado):
        """
        Verifica si el estado es objetivo, es decir, si todas las cajas están en los objetivos.
        """
        return estado["cajas"] == estado["objetivos"]

    def heuristica(self, estado):
        """
        Calcula la heurística del estado (distancia de Manhattan de cada caja al objetivo más cercano).
        """
        total_distancia = 0
        for caja in estado["cajas"]:
            distancias = [
                abs(caja[0] - obj[0]) + abs(caja[1] - obj[1])
                for obj in estado["objetivos"]
            ]
            total_distancia += min(distancias)
        return total_distancia

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

    def resolver(self):
        """
        Ejecuta la búsqueda A* para encontrar la solución.
        """
        # Inicializar la cola de prioridad
        heap = []
        
        # Estado inicial y su costo
        g_cost = 0  # Costo inicial es 0
        f_cost = g_cost + self.heuristica(self.estado_inicial)
        
        # Insertar el estado inicial en la cola de prioridad
        # La tupla (f_cost, g_cost, camino, estado) evita comparar los diccionarios directamente
        heapq.heappush(heap, (f_cost, g_cost, "", self.estado_inicial))  # (f, g, camino, estado)
        
        # Conjunto para rastrear estados visitados
        visited = set()
        visited.add((self.estado_inicial['jugador'], frozenset(self.estado_inicial['cajas'])))
        
        while heap:
            # Extraer el estado con el menor f(n)
            f_cost, g_cost, camino, estado_actual = heapq.heappop(heap)
            
            # Verificar si hemos alcanzado el objetivo
            if self.es_estado_objetivo(estado_actual):
                return camino   # Devuelve el camino en LURD si encontró una solución
            
            # Generar nuevos estados (movimientos válidos)
            for nuevo_estado, direccion in self.generar_movimientos(estado_actual):
                estado_clave = (nuevo_estado['jugador'], frozenset(nuevo_estado['cajas']))
                
                # Si el estado no ha sido visitado, agrégalo a la cola y a los visitados
                if estado_clave not in visited:
                    visited.add(estado_clave)
                    nuevo_g_cost = g_cost + 1  # Cada movimiento tiene un costo de 1
                    nuevo_f_cost = nuevo_g_cost + self.heuristica(nuevo_estado)
                    heapq.heappush(heap, (nuevo_f_cost, nuevo_g_cost, camino + direccion, nuevo_estado))
                    
        return None  # Si no se encuentra solución, devuelve None