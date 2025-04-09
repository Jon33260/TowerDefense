import pygame
import math
from map import WAYPOINTS  # Importer WAYPOINTS

class Enemy:
    def __init__(self):
        self.waypoints = WAYPOINTS
        self.index = 0
        self.pos = list(self.waypoints[0])  # Convertir en liste pour pouvoir modifier
        self.speed = 2
        self.health = 1000  # Santé de l'ennemi

    def take_damage(self, damage):
        """Infliger des dégâts à l'ennemi."""
        self.health -= damage
        if self.health <= 0:
            self.health = 0  # Optionnel : pour éviter des valeurs négatives de santé
            # Optionnel : ajouter ici la logique pour tuer l'ennemi, comme sa suppression de la liste

    def update(self):
        if self.index < len(self.waypoints) - 1:
            target = self.waypoints[self.index + 1]
            dx = target[0] - self.pos[0]
            dy = target[1] - self.pos[1]
            distance = math.sqrt(dx**2 + dy**2)  # Calcul de la distance

            if distance < self.speed:
                self.pos = list(target)  # Placer l'ennemi directement sur le waypoint
                self.index += 1
            else:
                direction = (dx / distance, dy / distance)
                self.pos[0] += direction[0] * self.speed
                self.pos[1] += direction[1] * self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (int(self.pos[0]), int(self.pos[1])), 15)
