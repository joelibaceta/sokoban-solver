import time
from collections import deque
from strategies.strategy import Strategy

class IDAStarStrategy(Strategy):

    def heuristica(self, estado):
        """
        Calcula la heurística del estado (distancia de Manhattan de cada caja al objetivo más cercano).
        """
        total_distancia = 0
        for caja in estado['cajas']:
            distancias = [abs(caja[0] - obj[0]) + abs(caja[1] - obj[1]) for obj in estado['objetivos']]
            total_distancia += min(distancias)
        return total_distancia

    def profundidad_limitada(self, estado, camino, g_cost, limite, visitados):
        """
        Realiza búsqueda en profundidad limitada al costo.
        """
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
                resultado = self.profundidad_limitada(nuevo_estado, camino + direccion, g_cost + 1, limite, visitados)
                
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
            resultado = self.profundidad_limitada(self.estado_inicial, "", 0, limite, visitados)
            
            # Si se encuentra un camino (solución), se devuelve
            if isinstance(resultado, str):
                fin = time.time()
                tiempo_total = fin - inicio
                print(f"Solución encontrada en {tiempo_total:.2f} segundos")
                return super().preparar_respuesta(resultado)
            
            # Si no, actualiza el límite al mínimo valor f(n) que excedió el límite anterior
            if resultado == float('inf'):
                return super().preparar_respuesta(None)
            
            limite = resultado  # Actualiza el límite
            self.profundidad_maxima = max(self.profundidad_maxima, limite)  # Actualizar la profundidad máxima