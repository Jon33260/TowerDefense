import pygame
import math

class Projectile:
    def __init__(self, x, y, target):
        self.x = x
        self.y = y
        self.target = target
        self.speed = 5
        self.damage = 100

    def update(self):
        # Calculer la direction vers l'ennemi
        dx = self.target.pos[0] - self.x
        dy = self.target.pos[1] - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance < self.speed:  # Si le projectile atteint l'ennemi
            self.target.take_damage(self.damage)  # Infliger des dégâts
            return True  # Supprimer le projectile
        else:
            direction = (dx / distance, dy / distance)
            self.x += direction[0] * self.speed
            self.y += direction[1] * self.speed
            return False

    def draw(self, screen):
        # Dessiner le projectile
        pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), 5)
