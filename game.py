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
        self.castle_health = 100  # PV du château
        self.castle_image = pygame.image.load("assets/chateau.jpeg").convert_alpha()
        self.castle_image = pygame.transform.scale(self.castle_image, (60, 60))

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
            self.draw()  # Appel de la méthode draw pour redessiner l'écran

            if self.castle_health <= 0:  # Condition de Game Over
                self.display_game_over()  # Affiche la page Game Over
                pygame.display.update()  # Met à jour l'écran
                self.wait_for_restart()  # Attend une touche pour redémarrer

    def update(self):
        # Gestion du spawn des ennemis
        self.spawn_timer += 3
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 1
            self.enemies.append(Enemy())  # Crée un nouvel ennemi

        # Mettre à jour tous les ennemis
        for enemy in self.enemies:
            enemy.update()

        # Vérifier si un ennemi atteint la fin du chemin
        for enemy in self.enemies[:]:
            dx = enemy.pos[0] - WAYPOINTS[-1][0]
            dy = enemy.pos[1] - WAYPOINTS[-1][1]
            distance = (dx**2 + dy**2) ** 0.5

            if distance < 10:  # Rayon d'arrivée au château
                self.enemies.remove(enemy)
                self.castle_health -= 10  # Réduit la vie du château

        # Si un ennemi est tué, on gagne de l'argent
        for enemy in self.enemies[:]:
            if enemy.health <= 0:
                self.enemies.remove(enemy)
                self.money += 20  # Récompense pour l'ennemi tué

        # Mettre à jour toutes les tours
        for tower in self.towers:
            tower.update(self.enemies)

    def draw(self):
        """ Dessine tous les éléments à l'écran """
        self.screen.fill((34, 139, 34))  # fond vert
        self.draw_path()

        # Dessiner le château
        castle_pos = WAYPOINTS[-1]
        castle_rect = self.castle_image.get_rect(center=castle_pos)
        self.screen.blit(self.castle_image, castle_rect)

        # Dessiner les tours
        for tower in self.towers:
            tower.update(self.enemies)  # Mettre à jour la tour, y compris le cercle du rayon d'attaque
            tower.draw(self.screen)     # Dessiner la tour elle-même

        # Dessiner les ennemis
        for enemy in self.enemies:
            enemy.draw(self.screen)

        # Afficher l'argent et les PV du château
        font = pygame.font.SysFont(None, 36)
        money_text = font.render(f"Argent: ${self.money}", True, (255, 255, 255))
        self.screen.blit(money_text, (10, 10))

        castle_text = font.render(f"Château: {self.castle_health} PV", True, (255, 255, 255))
        self.screen.blit(castle_text, (10, 50))

        pygame.display.flip()

    def draw_path(self):
        """ Dessine le chemin emprunté par les ennemis """
        for i in range(len(WAYPOINTS) - 1):
            pygame.draw.line(
                self.screen, (200, 200, 0),
                WAYPOINTS[i], WAYPOINTS[i + 1], 20
            )

    def display_game_over(self):
        """ Affiche l'écran de Game Over """
        font = pygame.font.SysFont(None, 72)
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        restart_text = pygame.font.SysFont(None, 36).render("Appuyez sur R pour redémarrer", True, (255, 255, 255))

        self.screen.fill((0, 0, 0))  # Fond noir
        self.screen.blit(game_over_text, (self.screen.get_width() // 2 - game_over_text.get_width() // 2, self.screen.get_height() // 2 - game_over_text.get_height() // 2))
        self.screen.blit(restart_text, (self.screen.get_width() // 2 - restart_text.get_width() // 2, self.screen.get_height() // 2 + 50))

        pygame.display.flip()

    def wait_for_restart(self):
        """ Attend la touche 'R' pour redémarrer le jeu """
        waiting_for_restart = True
        while waiting_for_restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting_for_restart = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Si "R" est pressé
                        self.reset_game()  # Réinitialise le jeu
                        waiting_for_restart = False

    def reset_game(self):
        """ Réinitialise le jeu pour le redémarrer """
        self.money = 100
        self.castle_health = 100
        self.towers = []
        self.enemies = []
        self.spawn_timer = 0
        # Nous n'arrêtons pas le jeu ici, cela va reprendre sans fermer la fenêtre
