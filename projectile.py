import pygame
import math

class Projectile:
    def __init__(self, x, y, target):
        self.x = x
        self.y = y
        self.target = target
        self.speed = 5
        self.damage = 100

        # Charge l'image de flèche
        self.image = pygame.image.load("assets/fleche.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 10))  # Ajuste la taille selon ton image

    def update(self):
        dx = self.target.pos[0] - self.x
        dy = self.target.pos[1] - self.y
        distance = math.hypot(dx, dy)

        if distance < self.speed:
            self.target.take_damage(self.damage)
            return True
        else:
            direction = (dx / distance, dy / distance)
            self.x += direction[0] * self.speed
            self.y += direction[1] * self.speed
            return False

    def draw(self, screen):
        # Calcule l'angle pour faire pivoter la flèche vers la cible
        angle = math.degrees(math.atan2(-(self.target.pos[1] - self.y), self.target.pos[0] - self.x))
        rotated_image = pygame.transform.rotate(self.image, angle)

        # Centrer l'image sur le projectile
        rect = rotated_image.get_rect(center=(self.x, self.y))
        screen.blit(rotated_image, rect)
