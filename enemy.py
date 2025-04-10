import pygame
import math
from map import WAYPOINTS

class Enemy:
    def __init__(self, enemy_type="normal"):
        self.type = enemy_type
        self.index = 0
        # Conversion explicite en liste ici
        self.pos = list(WAYPOINTS[self.index])  # Toujours convertir en liste
        self.set_stats_by_type()

        # Choix de l'image selon le type
        if self.type == "boss":
            img_path = "assets/boss.png"
        elif self.type == "mini-boss":
            img_path = "assets/ennemies/miniBoss.png"
        else:
            img_path = "assets/ennemies/gobelinPython.png"

        self.image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))

    def set_stats_by_type(self):
        if self.type == "normal":
            self.health = 1600
            self.speed = 3
            self.reward = 50
        elif self.type == "mini-boss":
            self.health = 2000
            self.speed = 2
            self.reward = 150
        elif self.type == "boss":
            self.health = 3000
            self.speed = 1
            self.reward = 500

    def update(self):
        """Met à jour la position de l'ennemi selon les waypoints."""
        print(f"self.pos avant mise à jour: {self.pos} (type: {type(self.pos)})")  # Debug

        # Assurez-vous que `self.pos` est bien une liste avant toute modification
        if not isinstance(self.pos, list):
            self.pos = list(self.pos)  # Force conversion en liste si ce n'est pas déjà une liste

        if self.index < len(WAYPOINTS) - 1:
            target = WAYPOINTS[self.index + 1]
            dx = target[0] - self.pos[0]
            dy = target[1] - self.pos[1]
            distance = math.hypot(dx, dy)

            if distance > self.speed:
                dx /= distance
                dy /= distance
                # Modification de `self.pos` qui doit être une liste
                self.pos[0] += dx * self.speed
                self.pos[1] += dy * self.speed
            else:
                self.index += 1
                if self.index < len(WAYPOINTS):
                    # Conversion explicite en liste à chaque changement d'index
                    self.pos = list(WAYPOINTS[self.index])  # Conversion explicite en liste
                    print(f"self.pos après mise à jour: {self.pos} (type: {type(self.pos)})")  # Debug

    def take_damage(self, amount):
        self.health -= amount

    def draw(self, screen):
        # Affichage de l'image de l'ennemi
        enemy_rect = self.image.get_rect(center=self.pos)
        screen.blit(self.image, enemy_rect)

        # Paramètres de la barre de vie
        bar_height = 5  # Hauteur fixe pour la barre de vie
        max_bar_width = 30  # Largeur maximale de la barre de vie, ajustée selon l'ennemi
        health_ratio = max(0, self.health / self.max_health)  # Ratio de vie restant

        # Calcul de la largeur de la barre de vie en fonction de la santé
        health_bar_width = max_bar_width * health_ratio

        # Calcul de la position de la barre de vie (juste au-dessus de l'ennemi)
        health_bar = pygame.Rect(self.pos[0] - max_bar_width / 2, self.pos[1] - 30, health_bar_width, bar_height)
        border = pygame.Rect(self.pos[0] - max_bar_width / 2, self.pos[1] - 30, max_bar_width, bar_height)

        # Dessiner la barre de vie (en rouge)
        pygame.draw.rect(screen, (255, 0, 0), health_bar)

        # Dessiner le bord de la barre de vie (en blanc)
        pygame.draw.rect(screen, (255, 255, 255), border, 1)


    @property
    def max_health(self):
        return {
            "normal": 1600,
            "mini-boss": 2000,
            "boss": 3000
        }.get(self.type, 100)
