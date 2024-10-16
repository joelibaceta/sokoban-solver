import pygame
from strategies.bfs import BFSStrategy

class Game:

    def __init__(self):
        self.lurd_history = []

    def load_level(self, level_path):
        # Cargar el nivel desde un archivo
        level = open(level_path, 'r')
        self.level_data = [list(line.rstrip()) for line in level.readlines()]
        level.close()
        # Configurar la ventana acorde al tamaño del nivel
        width = max(map(len, self.level_data)) * 36
        height = len(self.level_data) * 36
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Sokoban')

        return self.level_data
    
    def autoplay(self):
        bfs = BFSStrategy(self.level_data)
        solucion = bfs.resolver()
        for movimiento in solucion:
            self.movePlayer(movimiento)
            self.draw()
            pygame.time.wait(200)

    def draw(self):
        # Cargar imagenes de los elementos
        wall = pygame.image.load('images/wall.png')
        player = pygame.image.load('images/player.png')
        player_target = pygame.image.load('images/player.png')
        target = pygame.image.load('images/target.png')
        box = pygame.image.load('images/box.png')
        box_target = pygame.image.load('images/box_target.png')
        space = pygame.image.load('images/space.png')

        xcb = {"#": wall, "@": player, ".": target, "+": player_target, "$": box, "*": box_target, " ": space}

        # Dibujar el nivel
        for y, row in enumerate(self.level_data):
            for x, char in enumerate(row):
                self.screen.blit(xcb[char], (x * 36, y * 36))

        pygame.display.flip()
    
    def get_player_position(self):
        for y, row in enumerate(self.level_data):
            for x, char in enumerate(row):
                if char in ('@', '+'):
                    return x, y

    def movePlayer(self, direction):
        player_x, player_y = self.get_player_position()
        current_position = self.level_data[player_y][player_x]

        # Calcular las nuevas posiciones basadas en la dirección
        if direction == 'L':
            target_x, target_y = player_x - 1, player_y
            next_x, next_y = player_x - 2, player_y
        elif direction == 'U':
            target_x, target_y = player_x, player_y - 1
            next_x, next_y = player_x, player_y - 2
        elif direction == 'R':
            target_x, target_y = player_x + 1, player_y
            next_x, next_y = player_x + 2, player_y
        elif direction == 'D':
            target_x, target_y = player_x, player_y + 1
            next_x, next_y = player_x, player_y + 2
        else:
            return False  # Dirección no válida

        # Movimiento sin caja
        if self.level_data[target_y][target_x] in (' ', '.'):
            # Dejar la casilla original como estaba
            self.level_data[player_y][player_x] = '.' if current_position == '+' else ' '
            # Actualizar la nueva posición del jugador
            self.level_data[target_y][target_x] = '+' if self.level_data[target_y][target_x] == '.' else '@'
            self.lurd_history.append(direction.lower())
            return True

        # Movimiento con caja
        if self.level_data[target_y][target_x] in ('$', '*') and self.level_data[next_y][next_x] in (' ', '.'):
            # Dejar la casilla original como estaba
            self.level_data[player_y][player_x] = '.' if current_position == '+' else ' '
            # Mover la caja
            self.level_data[next_y][next_x] = '*' if self.level_data[next_y][next_x] == '.' else '$'
            # Mover el jugador
            self.level_data[target_y][target_x] = '+' if self.level_data[target_y][target_x] == '*' else '@'
            self.lurd_history.append(direction.upper())
            return True

        return False  # Movimiento inválido