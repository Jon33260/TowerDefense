import pygame
import math

class Tower:
    def __init__(self, x, y):
        self.x = x  # Position de la tour
        self.y = y
        self.range = 100  # Portée de la tour
        self.tower_image = pygame.image.load("assets/towers/tourPython.png").convert_alpha()  # Image de la tour
        
        # Obtenir la taille actuelle de l'image
        width, height = self.tower_image.get_size()
        
        # Diviser la taille par 2
        new_width = width // 2
        new_height = height // 2
        
        # Redimensionner l'image de la tour
        self.tower_image = pygame.transform.scale(self.tower_image, (new_width, new_height))

        # Définir le rect de la tour avec la nouvelle taille
        self.rect = self.tower_image.get_rect(center=(self.x, self.y))  # Rectangle de la tour avec les nouvelles dimensions

    def is_in_range(self, enemy):
        """ Vérifie si l'ennemi est dans la portée de la tour """
        dx = self.x - enemy.pos[0]
        dy = self.y - enemy.pos[1]
        distance = (dx**2 + dy**2) ** 0.5
        return distance <= self.range

    def update(self, enemies):
        """ Met à jour la logique de la tour (tirer sur les ennemis dans la portée) """
        for enemy in enemies:
            if self.is_in_range(enemy):
                self.attack(enemy)

    def attack(self, enemy):
        """ Attaque l'ennemi """
        enemy.health -= 10
        if enemy.health <= 0:
            print(f"Enemy destroyed at position ({enemy.pos[0]}, {enemy.pos[1]})")

    def draw(self, screen):
        """ Dessine la tour sur l'écran """
        screen.blit(self.tower_image, self.rect)
