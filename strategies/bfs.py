from collections import deque

class BFSStrategy:

    def __init__(self, mapa):
        # Estado inicial del juego: posiciones del jugador y cajas
        self.estado_inicial = self.mapa_a_estado(mapa)
        # Cola para la búsqueda en amplitud, incluye el camino recorrido
        self.queue = deque([(self.estado_inicial, "")])  # Empareja el estado con el camino inicial vacío
        # Conjunto para mantener los estados visitados
        self.visited = set()
        # Agregar el estado inicial a los visitados
        self.visited.add((self.estado_inicial['jugador'], frozenset(self.estado_inicial['cajas'])))

    def mapa_a_estado(self, mapa):
        """
        Convierte el mapa del nivel en un estado del juego.
        """
        jugador = None
        cajas = set()
        objetivos = set()
        paredes = set()
        
        for y, row in enumerate(mapa):
            for x, char in enumerate(row):
                if char in ('@', '+'):
                    jugador = (x, y)
                if char in ('$', '*'):
                    cajas.add((x, y))
                if char in ('.', '+', '*'):
                    objetivos.add((x, y))
                if char == '#':
                    paredes.add((x, y))
        
        return {
            'jugador': jugador,
            'cajas': cajas,
            'objetivos': objetivos,
            'paredes': paredes
        }

    def es_estado_objetivo(self, estado):
        """
        Verifica si el estado es objetivo, es decir, si todas las cajas están en los objetivos.
        """
        return estado['cajas'] == estado['objetivos']

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

    def resolver(self):
        """
        Ejecuta la búsqueda en amplitud para encontrar la solución.
        """
        while self.queue:
            estado_actual, camino = self.queue.popleft()

            print(camino)  # Imprimir el camino recorrido
            
            # Verificar si hemos alcanzado el objetivo
            if self.es_estado_objetivo(estado_actual):
                return camino   # Devuelve el camino en LURD si encontró una solución
            
            # Generar nuevos estados (movimientos válidos)
            for nuevo_estado, direccion in self.generar_movimientos(estado_actual):
                estado_clave = (nuevo_estado['jugador'], frozenset(nuevo_estado['cajas']))
                
                # Si el estado no ha sido visitado, agrégalo a la cola y a los visitados
                if estado_clave not in self.visited:
                    self.visited.add(estado_clave)
                    self.queue.append((nuevo_estado, camino + direccion))  # Añadir la dirección al camino
                    
        return None  # Si no se encuentra solución, devuelve None