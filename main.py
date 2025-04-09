import pygame
from game import Game

def main():
    pygame.init()  # ← Important ! Initialise Pygame
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Tower Defense")
    game = Game(screen)
    game.run()
    pygame.quit()  # ← proprement quitter pygame à la fin

if __name__ == "__main__":
    main()