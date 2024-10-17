import time
from collections import deque
from strategies.strategy import Strategy

class IDDFSStrategy(Strategy):
    """
    ## Búsqueda en Profundidad Iterativa (IDDFS)

    - **Objetivo:** IDDFS combina la profundidad limitada de DFS con la búsqueda completa de BFS, evitando la acumulación de nodos que se da en BFS.
	- **Método:** Realiza una búsqueda en profundidad hasta un límite determinado. Si no encuentra la solución, aumenta el límite y repite, volviendo a explorar desde el nodo inicial. Es una combinación de DFS y BFS, ya que actúa como DFS en cada iteración, pero explora niveles de manera similar a BFS al incrementar el límite.
	- **Optimalidad:** Al igual que BFS, garantiza la solución más corta en términos de pasos en problemas no ponderados.
	- **Ventaja:** Consume mucha menos memoria que BFS, ya que solo mantiene los nodos actuales en la pila.
	- **Desventaja:** Requiere revisitar muchos nodos a medida que incrementa el límite, lo que puede hacerlo más lento que BFS en algunos casos.
    """

    def profundidad_limitada(self, estado, camino, limite, visitados):
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
        visitados.add(estado_clave)

        for nuevo_estado, direccion in self.generar_movimientos(estado):
            nuevo_estado_clave = (
                nuevo_estado["jugador"],
                frozenset(nuevo_estado["cajas"]),
            )

            # Si el estado no ha sido visitado en este nivel de profundidad
            if nuevo_estado_clave not in visitados:
                self.nodos_abiertos += 1  # Incrementar nodos abiertos
                resultado = self.profundidad_limitada(
                    nuevo_estado, camino + direccion, limite - 1, visitados
                )
                
                # Si encuentra una solución, la devuelve
                if resultado is not None:
                    return resultado

        self.nodos_cerrados += 1  # Incrementar nodos cerrados al finalizar la expansión de este nodo
        return None

    def resolver(self):
        """
        Ejecuta la búsqueda en profundidad iterativa para encontrar la solución.
        """
        inicio = time.time()  # Tiempo de inicio
        limite = 0  # Empieza con profundidad 0
        
        while True:
            visitados = set()  # Reiniciar el conjunto de visitados para cada límite
            self.profundidad_maxima = max(self.profundidad_maxima, limite)  # Actualizar la profundidad máxima
            resultado = self.profundidad_limitada(
                self.estado_inicial, "", limite, visitados
            )

            # Si encuentra la solución, imprime y retorna el resultado
            if resultado is not None:
                fin = time.time()
                self.tiempo_total = fin - inicio
                return super().preparar_respuesta(resultado)

            # Aumenta el límite y sigue buscando
            limite += 1