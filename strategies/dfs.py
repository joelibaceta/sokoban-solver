import time
from collections import deque
from strategies.strategy import Strategy

class DFSStrategy(Strategy):
    """
    ## Búsqueda en Profundidad (DFS)
    
    - **Objetivo:** DFS se enfoca en profundizar en un camino hasta que no puede continuar, luego retrocede y explora otros caminos. Su objetivo es explorar completamente un camino antes de probar otros.
	- **Método:** Utiliza una pila (explícita o implícita en la recursión) para profundizar hasta que llega a un final, luego retrocede (backtracking) y prueba otras rutas.
	- **Optimalidad:** No garantiza encontrar la solución más corta. Puede encontrar cualquier solución en su camino de exploración, y si encuentra varias, no asegura que sea la más corta.
	- **Ventaja:** Requiere poca memoria, ya que solo mantiene los nodos actuales en la pila.
	- **Desventaja:** Puede quedar atrapado en ciclos o en un camino de gran profundidad, y no tiene garantía de optimalidad. Además, si el espacio de búsqueda es infinito, puede correr indefinidamente sin encontrar la solución.
    """

    def __init__(self, mapa):
        super().__init__(mapa)
        # Pila para la búsqueda en profundidad, incluye el camino recorrido y la profundidad
        self.stack = deque([(self.estado_inicial, "", 0)])  # (estado, camino, profundidad)
        # Conjunto para mantener los estados visitados
        self.visited = set()
        # Agregar el estado inicial a los visitados
        self.visited.add((self.estado_inicial["jugador"], frozenset(self.estado_inicial["cajas"])))

    def resolver(self):
        """
        Ejecuta la búsqueda en profundidad para encontrar la solución.
        """
        # Iniciar el tiempo de cálculo
        inicio = time.time()
        
        while self.stack:
            estado_actual, camino, profundidad = self.stack.pop()
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
                estado_clave = (
                    nuevo_estado["jugador"],
                    frozenset(nuevo_estado["cajas"]),
                )

                # Si el estado no ha sido visitado, agrégalo a la pila y a los visitados
                if estado_clave not in self.visited:
                    self.visited.add(estado_clave)
                    self.stack.append((nuevo_estado, camino + direccion, profundidad + 1))  # (estado, camino, profundidad)
                    self.nodos_abiertos += 1  # Incrementar los nodos abiertos

        # Si no se encuentra solución
        fin = time.time()
        self.tiempo_total = fin - inicio
        return super().preparar_respuesta(None)