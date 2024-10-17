import time
import heapq
from collections import deque
from strategies.strategy import Strategy

class AStarStrategy(Strategy):
    """
    ## A*

    - **Objetivo:** A* es un algoritmo de búsqueda informada que utiliza una función heurística para estimar el costo desde el estado actual hasta el estado objetivo. Su objetivo es encontrar la ruta más corta hacia el objetivo.
    - **Método:** A* expande los nodos en función de un valor f(n) = g(n) + h(n), donde:
        - g(n) es el costo exacto desde el nodo inicial hasta n.
        - h(n) es una heurística que estima el costo desde n hasta el objetivo.
    - **Optimalidad:** Si la heurística es admisible (es decir, nunca sobreestima el costo real), A* garantiza encontrar la solución óptima.
    - **Ventaja:** Enfoca la búsqueda en el camino con el menor costo estimado hacia el objetivo, reduciendo el número de nodos a explorar.
    - **Desventaja:** A* consume mucha memoria, ya que debe mantener todos los nodos en la cola de prioridad hasta encontrar la solución. En problemas con grandes espacios de búsqueda, esto puede llevar a un uso excesivo de recursos.
    """

    def heuristica(self, estado):
        """
        Calcula la heurística del estado (distancia de Manhattan de cada caja al objetivo más cercano).
        """
        total_distancia = 0
        for caja in estado['cajas']:
            distancias = [abs(caja[0] - obj[0]) + abs(caja[1] - obj[1]) for obj in estado['objetivos']]
            total_distancia += min(distancias)
        return total_distancia

    def resolver(self):
        """
        Ejecuta la búsqueda A* para encontrar la solución.
        """
        inicio = time.time()  # Tiempo de inicio
        
        # Inicializar la cola de prioridad
        heap = []
        
        # Estado inicial y su costo
        g_cost = 0  # Costo inicial es 0
        f_cost = g_cost + self.heuristica(self.estado_inicial)
        
        # Insertar el estado inicial en la cola de prioridad
        heapq.heappush(heap, (f_cost, g_cost, 0, "", self.estado_inicial))  # (f, g, profundidad, camino, estado)
        
        # Conjunto para rastrear estados visitados
        visited = set()
        visited.add((self.estado_inicial['jugador'], frozenset(self.estado_inicial['cajas'])))
        
        while heap:
            # Extraer el estado con el menor f(n)
            f_cost, g_cost, profundidad, camino, estado_actual = heapq.heappop(heap)
            self.nodos_cerrados += 1  # Incrementar nodos cerrados
            
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
                estado_clave = (nuevo_estado['jugador'], frozenset(nuevo_estado['cajas']))
                
                # Si el estado no ha sido visitado, agrégalo a la cola y a los visitados
                if estado_clave not in visited:
                    visited.add(estado_clave)
                    nuevo_g_cost = g_cost + 1  # Cada movimiento tiene un costo de 1
                    nuevo_f_cost = nuevo_g_cost + self.heuristica(nuevo_estado)
                    heapq.heappush(heap, (nuevo_f_cost, nuevo_g_cost, profundidad + 1, camino + direccion, nuevo_estado))
                    self.nodos_abiertos += 1  # Incrementar nodos abiertos

        # Si no se encuentra solución
        fin = time.time()
        self.tiempo_total = fin - inicio
        return super().preparar_respuesta(None)