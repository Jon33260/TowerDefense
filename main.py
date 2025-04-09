import pygame
from game import Game

def main_menu(screen):
    """Affiche le menu principal et attend que l'utilisateur clique sur 'Jouer'."""
    font = pygame.font.SysFont(None, 74)
    title_text = font.render("Tower Defense", True, (255, 255, 255))
    play_button = font.render("Jouer", True, (0, 255, 0))
    play_button_rect = play_button.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))

    # Charger l'image de fond avec gestion des erreurs
    try:
        background = pygame.image.load("assets/accueil.jpeg").convert()
        background = pygame.transform.scale(background, (800, 600))  # Ajuste la taille au besoin
    except pygame.error as e:
        print(f"Erreur de chargement de l'image : {e}")
        return  # Si l'image ne se charge pas, on arrête la fonction

    while True:
        screen.fill((0, 0, 0))  # Fond noir
        screen.blit(background, (0, 0))  # Affiche l'image de fond
        screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, screen.get_height() // 2 - 100))
        screen.blit(play_button, play_button_rect.topleft)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    return True

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Tower Defense")

    if main_menu(screen):
        game = Game(screen)
        game.run()

    pygame.quit()

if __name__ == "__main__":
    main()
