import pygame
import math
from projectile import Projectile

class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = 150  # Portée de la tour
        self.attack_speed = 60  # Vitesse d'attaque en frames
        self.projectiles = []  # Liste des projectiles
        self.last_shot_time = 0

    def update(self, enemies):
        # Chercher l'ennemi le plus proche dans la portée de la tour
        for enemy in enemies:
            distance = math.sqrt((enemy.pos[0] - self.x) ** 2 + (enemy.pos[1] - self.y) ** 2)
            if distance <= self.range:
                self.shoot(enemy)  # Tirer sur l'ennemi

        # Mettre à jour les projectiles
        self.projectiles = [p for p in self.projectiles if not p.update()]  # Retirer les projectiles touchés

    def shoot(self, enemy):
        # Créer un projectile qui va vers l'ennemi
        if pygame.time.get_ticks() - self.last_shot_time > self.attack_speed:
            self.projectiles.append(Projectile(self.x, self.y, enemy))
            self.last_shot_time = pygame.time.get_ticks()  # Mise à jour du temps du dernier tir

    def draw(self, screen):
        # Dessiner la tour (par exemple, un cercle)
        pygame.draw.circle(screen, (0, 0, 255), (self.x, self.y), 20)

        # Dessiner les projectiles
        for projectile in self.projectiles:
            projectile.draw(screen)
