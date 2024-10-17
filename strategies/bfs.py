import time
from collections import deque
from strategies.strategy import Strategy

class BFSStrategy(Strategy):
    """
    ## Búsqueda en Amplitud (BFS)

    - **Objetivo:** BFS es un algoritmo de búsqueda no informada que expande nodos en función de su distancia al nodo inicial, buscando niveles completos antes de avanzar al siguiente.
	- **Método:** Explora todos los nodos a una cierta distancia del inicial antes de profundizar más. Utiliza una cola para manejar los nodos a expandir.
	- **Optimalidad:** BFS garantiza la solución más corta en problemas no ponderados (es decir, donde cada paso tiene el mismo costo).
	- **Ventaja:** Encuentra la solución más corta en términos de número de pasos y es relativamente simple de implementar.
	- **Desventaja:** Consume mucha memoria, ya que debe almacenar todos los nodos de cada nivel antes de pasar al siguiente, lo que puede ser ineficiente en problemas de gran escala.
    """

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
                self.tiempo_total = fin - inicio
                print(f"Solución encontrada en {self.tiempo_total:.2f} segundos")
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
        self.tiempo_total = fin - inicio
        return super().preparar_respuesta(None)