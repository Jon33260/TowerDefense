import pygame
from enemy import Enemy
from map import WAYPOINTS
from tower import Tower

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()
        self.money = 100  # Argent initial
        self.towers = []
        self.enemies = []
        self.spawn_timer = 0
        self.spawn_interval = 120  # frames

    def run(self):
        while self.running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clic gauche de la souris
                        pos = pygame.mouse.get_pos()
                        # Vérifie si on a assez d'argent pour acheter une tour
                        tower_cost = 50  # Exemple de coût d'une tour
                        if self.money >= tower_cost:
                            self.towers.append(Tower(pos[0], pos[1]))  # Crée une tour
                            self.money -= tower_cost  # Réduit l'argent du joueur

            self.update()
            self.draw()

    def update(self):
        # Gestion du spawn des ennemis
        self.spawn_timer += 3
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 1
            self.enemies.append(Enemy())

        # Mettre à jour tous les ennemis
        for enemy in self.enemies:
            enemy.update()

        # Vérifier si l'ennemi atteint la fin du chemin
        for enemy in self.enemies[:]:
            if enemy.pos == WAYPOINTS[-1]:  # L'ennemi a atteint la fin du chemin
                self.enemies.remove(enemy)
                self.money -= 10  # Perdre de l'argent pour un ennemi passé

        # Si un ennemi est tué, on gagne de l'argent
        for enemy in self.enemies[:]:
            if enemy.health <= 0:
                self.enemies.remove(enemy)
                self.money += 20  # Récompense pour l'ennemi tué

        # Mettre à jour toutes les tours
        for tower in self.towers:
            tower.update(self.enemies)


    def draw(self):
        self.screen.fill((34, 139, 34))  # fond vert
        self.draw_path()

        # Dessiner les tours
        for tower in self.towers:
            tower.draw(self.screen)

        # Dessiner les ennemis
        for enemy in self.enemies:
            enemy.draw(self.screen)

        # Afficher l'argent du joueur
        font = pygame.font.SysFont(None, 36)
        money_text = font.render(f"Argent: ${self.money}", True, (255, 255, 255))
        self.screen.blit(money_text, (10, 10))  # Affiche l'argent en haut à gauche

        pygame.display.flip()

    def draw_path(self):
        for i in range(len(WAYPOINTS) - 1):
            pygame.draw.line(
                self.screen, (200, 200, 0),
                WAYPOINTS[i], WAYPOINTS[i + 1], 20
            )
