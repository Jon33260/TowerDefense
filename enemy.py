import pygame
import math
from map import WAYPOINTS

class Enemy:
    def __init__(self, enemy_type="normal", speed=None):
        self.type = enemy_type
        self.index = 0
        self.pos = list(WAYPOINTS[self.index])  # Conversion explicite en liste

        if speed is not None:
            self.speed = speed
            self.health = self.max_health  # On utilise le max_health du type
            self.reward = {
                "normal": 50,
                "mini-boss": 150,
                "boss": 500
            }.get(self.type, 50)
        else:
            self.set_stats_by_type()  # Sinon on définit les stats basées sur le type

        # Debug : Vérifie si 'speed' et autres stats sont bien définis
        print(f"[DEBUG] Vitesse de l'ennemi ({self.type}): {self.speed}, Santé: {self.health}, Récompense: {self.reward}")

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
        """Définit les statistiques de l'ennemi en fonction de son type."""
        if self.type == "normal":
            self.health = 1600
            self.speed = 3
            self.reward = 50
        elif self.type == "mini-boss":
            self.health = 3000
            self.speed = 2
            self.reward = 150
        elif self.type == "boss":
            self.health = 4000
            self.speed = 1
            self.reward = 500

        print(f"[DEBUG] Stats de l'ennemi - Type: {self.type}, Vitesse: {self.speed}, Santé: {self.health}")

    def update(self):
        print(f"self.pos avant mise à jour: {self.pos} (type: {type(self.pos)})")  # Debug

        if not isinstance(self.pos, list):
            self.pos = list(self.pos)

        if self.index < len(WAYPOINTS) - 1:
            target = WAYPOINTS[self.index + 1]
            dx = target[0] - self.pos[0]
            dy = target[1] - self.pos[1]
            distance = math.hypot(dx, dy)

            if distance > self.speed:
                dx /= distance
                dy /= distance
                self.pos[0] += dx * self.speed
                self.pos[1] += dy * self.speed
            else:
                self.index += 1
                if self.index < len(WAYPOINTS):
                    self.pos = list(WAYPOINTS[self.index])
                    print(f"self.pos après mise à jour: {self.pos} (type: {type(self.pos)})")  # Debug

    def take_damage(self, amount):
        self.health -= amount

    def draw(self, screen):
        enemy_rect = self.image.get_rect(center=self.pos)
        screen.blit(self.image, enemy_rect)

        bar_height = 5
        max_bar_width = 30
        health_ratio = max(0, self.health / self.max_health)
        health_bar_width = max_bar_width * health_ratio

        health_bar = pygame.Rect(self.pos[0] - max_bar_width / 2, self.pos[1] - 30, health_bar_width, bar_height)
        border = pygame.Rect(self.pos[0] - max_bar_width / 2, self.pos[1] - 30, max_bar_width, bar_height)

        pygame.draw.rect(screen, (255, 0, 0), health_bar)
        pygame.draw.rect(screen, (255, 255, 255), border, 1)

    @property
    def max_health(self):
        return {
            "normal": 1400,
            "mini-boss": 2500,
            "boss": 3500
        }.get(self.type, 100)
