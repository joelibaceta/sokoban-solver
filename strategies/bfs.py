import time
from collections import deque
from strategies.strategy import Strategy

class BFSStrategy(Strategy):
    def __init__(self, mapa):
        super().__init__(mapa)
        # Cola para la búsqueda en amplitud, incluye el camino recorrido y la profundidad
        self.queue = deque([(self.estado_inicial, "", 0)])  # (estado, camino, profundidad)
        # Conjunto para mantener los estados visitados
        self.visited = set()
        # Agregar el estado inicial a los visitados
        self.visited.add((self.estado_inicial["jugador"], frozenset(self.estado_inicial["cajas"])))

    def resolver(self):
        """
        Ejecuta la búsqueda en amplitud para encontrar la solución.
        """
        # Iniciar el tiempo de cálculo
        inicio = time.time()
        
        while self.queue:
            estado_actual, camino, profundidad = self.queue.popleft()
            self.nodos_cerrados += 1  # Incrementar los nodos cerrados
            
            # Actualizar la profundidad máxima alcanzada
            if profundidad > self.profundidad_maxima:
                self.profundidad_maxima = profundidad

            # Verificar si hemos alcanzado el objetivo
            if self.es_estado_objetivo(estado_actual):
                fin = time.time()
                tiempo_total = fin - inicio
                print(f"Solución encontrada en {tiempo_total:.2f} segundos")
                return super().preparar_respuesta(camino)

            # Generar nuevos estados (movimientos válidos)
            for nuevo_estado, direccion in self.generar_movimientos(estado_actual):
                estado_clave = (nuevo_estado["jugador"], frozenset(nuevo_estado["cajas"]))

                # Si el estado no ha sido visitado, agrégalo a la cola y a los visitados
                if estado_clave not in self.visited:
                    self.visited.add(estado_clave)
                    self.queue.append((nuevo_estado, camino + direccion, profundidad + 1))  # (estado, camino, profundidad)
                    self.nodos_abiertos += 1  # Incrementar los nodos abiertos

        # Si no se encuentra solución
        fin = time.time()
        tiempo_total = fin - inicio
        return super().preparar_respuesta(None)