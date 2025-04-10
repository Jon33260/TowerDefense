import pygame

class Obstacle:
    def __init__(self, x, y, width, height):
        """Initialisation de l'obstacle.
        
        :param x: Position X de l'obstacle
        :param y: Position Y de l'obstacle
        :param width: Largeur de l'obstacle
        :param height: Hauteur de l'obstacle
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (139, 69, 19)  # Couleur marron pour l'obstacle

    def draw(self, screen):
        """Dessine l'obstacle sur l'écran."""
        pygame.draw.rect(screen, self.color, self.rect)

    def check_collision(self, other_rect):
        """Vérifie si l'obstacle entre en collision avec un autre objet (par exemple, le joueur ou les ennemis)."""
        return self.rect.colliderect(other_rect)
