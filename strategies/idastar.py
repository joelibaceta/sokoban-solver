from collections import deque
from strategies.strategy import Strategy

class IDAStarStrategy(Strategy):

    def __init__(self, mapa):
        # Estado inicial del juego: posiciones del jugador y cajas
        self.estado_inicial = super().mapa_a_estado(mapa)

    def es_estado_objetivo(self, estado):
        """
        Verifica si el estado es objetivo, es decir, si todas las cajas están en los objetivos.
        """
        return estado['cajas'] == estado['objetivos']

    def heuristica(self, estado):
        """
        Calcula la heurística del estado (distancia de Manhattan de cada caja al objetivo más cercano).
        """
        total_distancia = 0
        for caja in estado['cajas']:
            distancias = [abs(caja[0] - obj[0]) + abs(caja[1] - obj[1]) for obj in estado['objetivos']]
            total_distancia += min(distancias)
        return total_distancia

    def generar_movimientos(self, estado):
        """
        Genera movimientos válidos para el jugador y las cajas en el estado actual.
        """
        movimientos = []
        jugador_x, jugador_y = estado['jugador']
        
        # Movimientos posibles y sus correspondientes notaciones LURD
        desplazamientos = {
            "U": (0, -1),    # Arriba
            "D": (0, 1),     # Abajo
            "L": (-1, 0),    # Izquierda
            "R": (1, 0)      # Derecha
        }
        
        for direccion, (dx, dy) in desplazamientos.items():
            nuevo_jugador = (jugador_x + dx, jugador_y + dy)
            
            # Verifica si el movimiento es válido (no se sale del tablero ni choca con una pared)
            if nuevo_jugador not in estado['paredes']:
                # Si hay una caja en la posición, verifica si se puede empujar
                if nuevo_jugador in estado['cajas']:
                    nueva_caja = (nuevo_jugador[0] + dx, nuevo_jugador[1] + dy)
                    
                    # La nueva posición de la caja debe estar vacía y no ser una pared o caja
                    if nueva_caja not in estado['paredes'] and nueva_caja not in estado['cajas']:
                        nuevo_estado = {
                            'jugador': nuevo_jugador,
                            'cajas': estado['cajas'] - {nuevo_jugador} | {nueva_caja},
                            'objetivos': estado['objetivos'],
                            'paredes': estado['paredes']
                        }
                        movimientos.append((nuevo_estado, direccion))  # Agregar dirección al movimiento
                else:
                    # Si no hay caja, simplemente mueve el jugador
                    nuevo_estado = {
                        'jugador': nuevo_jugador,
                        'cajas': estado['cajas'],
                        'objetivos': estado['objetivos'],
                        'paredes': estado['paredes']
                    }
                    movimientos.append((nuevo_estado, direccion))  # Agregar dirección al movimiento
        
        return movimientos

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
                resultado = self.profundidad_limitada(nuevo_estado, camino + direccion, g_cost + 1, limite, visitados)
                
                # Si devuelve un camino (solución), lo propagamos hacia arriba
                if isinstance(resultado, str):
                    return resultado
                
                # De lo contrario, actualizamos el costo mínimo excedente
                min_costo_excedente = min(min_costo_excedente, resultado)
        
        # Remover el estado del conjunto visitado al retroceder (backtrack)
        visitados.remove(estado_clave)
        
        return min_costo_excedente

    def resolver(self):
        """
        Ejecuta la búsqueda IDA* para encontrar la solución.
        """
        limite = self.heuristica(self.estado_inicial)  # Límite inicial basado en la heurística del estado inicial
        
        while True:
            visitados = set()  # Reiniciar el conjunto de visitados para cada límite
            resultado = self.profundidad_limitada(self.estado_inicial, "", 0, limite, visitados)
            
            # Si se encuentra un camino (solución), se devuelve
            if isinstance(resultado, str):
                return resultado
            
            # Si no, actualiza el límite al mínimo valor f(n) que excedió el límite anterior
            if resultado == float('inf'):
                return None  # No hay solución
            limite = resultado  # Actualiza el límite