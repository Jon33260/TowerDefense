import pygame
import math
from map import WAYPOINTS  # Importer WAYPOINTS

class Enemy:
    def __init__(self):
        # Initialisation des propriétés de l'ennemi
        self.health = 1200
        self.speed = 2
        self.index = 0  # L'index du waypoint actuel
        self.pos = WAYPOINTS[self.index]  # Position initiale de l'ennemi à partir des waypoints
        self.image = pygame.image.load("assets/ennemies/gobelinPython.png").convert_alpha()  # Charger l'image de l'ennemi
        self.image = pygame.transform.scale(self.image, (40, 40))  # Redimensionner l'image si nécessaire

    def update(self):
        # L'ennemi se déplace le long des waypoints
        if self.index < len(WAYPOINTS) - 1:
            # Calcul de la direction vers le prochain waypoint
            target = WAYPOINTS[self.index + 1]
            dx = target[0] - self.pos[0]
            dy = target[1] - self.pos[1]
            distance = (dx**2 + dy**2) ** 0.5  # Calcul de la distance entre la position de l'ennemi et la cible

            # Déplacement de l'ennemi vers le prochain waypoint
            if distance > self.speed:
                dx /= distance
                dy /= distance
                self.pos = (self.pos[0] + dx * self.speed, self.pos[1] + dy * self.speed)  # Mise à jour de la position
            else:
                # Si l'ennemi est proche du waypoint, on passe au suivant
                self.index += 1
                if self.index < len(WAYPOINTS):  # Assure-toi qu'on ne dépasse pas le nombre de waypoints
                    self.pos = WAYPOINTS[self.index]

    def take_damage(self, amount):
        self.health -= amount  # 💥 Infliger les dégâts
    def draw(self, screen):
        # Afficher l'ennemi à sa position actuelle
        enemy_rect = self.image.get_rect(center=self.pos)  # Positionner l'image de l'ennemi
        screen.blit(self.image, enemy_rect)  # Dessiner l'ennemi à l'écran
