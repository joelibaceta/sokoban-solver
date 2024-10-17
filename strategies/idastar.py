import time
from collections import deque
from strategies.strategy import Strategy

class IDAStarStrategy(Strategy):
    """
    ## IDA*

    - **Objetivo:** IDA* busca reducir la memoria requerida por A* mediante un enfoque de profundidad iterativa en el que usa límites de costo en lugar de mantener una cola de prioridad.
	- **Método:** IDA* expande los nodos utilizando f(n) = g(n) + h(n) similar a A*, pero limita la profundidad (o el costo) que puede explorar en cada iteración. Si no encuentra la solución, aumenta el límite y reintenta.
	- **Optimalidad:** Como A*, si la heurística es admisible, IDA* garantiza una solución óptima.
	- **Ventaja:** Utiliza mucho menos memoria que A*, ya que solo mantiene los nodos en la pila de llamadas actual, liberando aquellos que ya no son necesarios.
	- **Desventaja:** Al tener que realizar varias iteraciones, revisita nodos repetidamente y puede ser más lento en problemas grandes. Sin embargo, es ideal para situaciones con limitaciones de memoria.
    """

    def __init__(self, mapa):
        super().__init__(mapa)
        self.tiempo_limite = 60  # Tiempo máximo en segundos

    def heuristica(self, estado):
        """
        Calcula la heurística del estado (distancia de Manhattan de cada caja al objetivo más cercano).
        """
        total_distancia = 0
        for caja in estado['cajas']:
            distancias = [abs(caja[0] - obj[0]) + abs(caja[1] - obj[1]) for obj in estado['objetivos']]
            total_distancia += min(distancias)
        return total_distancia

    def profundidad_limitada(self, estado, camino, g_cost, limite, visitados, inicio):
        """
        Realiza búsqueda en profundidad limitada al costo.
        """
        # Verificar el tiempo límite
        if time.time() - inicio > self.tiempo_limite:
            return "timeout"
        
        f_cost = g_cost + self.heuristica(estado)
        
        # Si el costo f(n) excede el límite, devolvemos el costo como límite siguiente
        if f_cost > limite:
            return f_cost
        
        # Verificar si hemos alcanzado el objetivo
        if self.es_estado_objetivo(estado):
            return camino   # Devuelve el camino en LURD si encontró una solución
        
        min_costo_excedente = float('inf')  # Inicializa el mínimo de los costos que exceden el límite
        
        # Marca este estado como visitado
        estado_clave = (estado['jugador'], frozenset(estado['cajas']))
        visitados.add(estado_clave)
        
        # Generar nuevos estados (movimientos válidos)
        for nuevo_estado, direccion in self.generar_movimientos(estado):
            nuevo_estado_clave = (nuevo_estado['jugador'], frozenset(nuevo_estado['cajas']))
            
            # Si el estado no ha sido visitado en este camino
            if nuevo_estado_clave not in visitados:
                self.nodos_abiertos += 1  # Incrementar nodos abiertos
                resultado = self.profundidad_limitada(nuevo_estado, camino + direccion, g_cost + 1, limite, visitados, inicio)
                
                # Si devuelve un camino (solución), lo propagamos hacia arriba
                if isinstance(resultado, str):
                    return resultado
                
                # De lo contrario, actualizamos el costo mínimo excedente
                min_costo_excedente = min(min_costo_excedente, resultado)
        
        # Remover el estado del conjunto visitado al retroceder (backtrack)
        visitados.remove(estado_clave)
        self.nodos_cerrados += 1  # Incrementar nodos cerrados al retroceder
        
        return min_costo_excedente

    def resolver(self):
        """
        Ejecuta la búsqueda IDA* para encontrar la solución.
        """
        inicio = time.time()  # Tiempo de inicio
        limite = self.heuristica(self.estado_inicial)  # Límite inicial basado en la heurística del estado inicial
        
        while True:
            visitados = set()  # Reiniciar el conjunto de visitados para cada límite
            resultado = self.profundidad_limitada(self.estado_inicial, "", 0, limite, visitados, inicio)
            
            # Si se encuentra un camino (solución), se devuelve
            if isinstance(resultado, str):
                if resultado == "timeout":
                    print("Tiempo límite alcanzado, deteniendo la búsqueda.")
                    return super().preparar_respuesta(None)

                fin = time.time()
                self.tiempo_total = fin - inicio
                print(f"Solución encontrada en {self.tiempo_total:.2f} segundos")
                return super().preparar_respuesta(resultado)
            
            # Si no, actualiza el límite al mínimo valor f(n) que excedió el límite anterior
            if resultado == float('inf'):  # No hay solución
                fin = time.time()
                self.tiempo_total = fin - inicio
                return super().preparar_respuesta(None)
            
            limite = resultado  # Actualiza el límite
            self.profundidad_maxima = max(self.profundidad_maxima, limite)  # Actualizar la profundidad máxima