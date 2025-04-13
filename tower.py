import pygame
import math
from projectile import Projectile

class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = 150  # Portée initiale de la tour
        self.fire_rate = 60  # Tir toutes les 60 frames
        self.cooldown = 0
        self.projectiles = []

        self.image = pygame.image.load("assets/towers/tourPython.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))  # Ajuste selon ta taille d'image

        # Attributs pour gérer l'amélioration
        self.level = 1
        self.base_damage = 10  # Dégâts de base
        self.damage = self.base_damage

    def update(self, enemies):
        if self.cooldown > 0:
            self.cooldown -= 1

        # Tir si possible
        target = self.get_target(enemies)
        if target and self.cooldown == 0:
            self.projectiles.append(Projectile(self.x, self.y, target))
            self.cooldown = self.fire_rate

        # Mise à jour des projectiles
        for projectile in self.projectiles[:]:
            if projectile.update():  # Si le projectile touche
                self.projectiles.remove(projectile)

    def get_target(self, enemies):
        """Retourne le premier ennemi dans la portée."""
        for enemy in enemies:
            dx = enemy.pos[0] - self.x
            dy = enemy.pos[1] - self.y
            distance = math.hypot(dx, dy)
            if distance <= self.range:
                return enemy
        return None

    def draw(self, screen):
        """Dessiner la tour et ses projectiles."""
        rect = self.image.get_rect(center=(self.x, self.y))
        screen.blit(self.image, rect)

        # Dessiner les projectiles
        for projectile in self.projectiles:
            projectile.draw(screen)

    def upgrade(self):
        """Améliorer la tour en augmentant ses caractéristiques."""
        self.level += 1
        self.range += 30  # Augmenter la portée
        self.fire_rate -= 5  # Réduire la période de tir (amélioration de la rapidité)
        self.damage += 5  # Augmenter les dégâts
