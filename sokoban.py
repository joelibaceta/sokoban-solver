import pygame
import sys
from game import Game

def main(level_path):

    # Inicializar Pygame
    pygame.init()
    
    # Cargar el nivel desde un archivo
    game = Game()
    game.load_level(level_path)

    autoplay_executed = False

    pygame.display.flip()

    game.draw()

    # Bucle del juego
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Ejecutar `autoplay` solo una vez
        if not autoplay_executed:
            game.autoplay()             # Se ejecuta solo la primera vez
            autoplay_executed = True    # Desactivar bandera para no volver a ejecutarlo
        
        # Dibujar el juego y actualizar pantalla
        game.draw()
        pygame.display.flip()


if __name__ == "__main__":
    # Leer nivel del archivo desde la línea de comandos
    level_path = sys.argv[1]
    # Inicializar el juego
    main(level_path)