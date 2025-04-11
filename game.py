import pygame
import math
from enemy import Enemy
from map import WAYPOINTS
from tower import Tower

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()
        self.money = 150
        self.towers = []
        self.enemies = []
        self.spawn_timer = 0
        self.spawn_interval = 120
        self.castle_health = 100
        self.castle_image = pygame.image.load("assets/chateau.png").convert_alpha()
        self.castle_image = pygame.transform.scale(self.castle_image, (60, 60))

        # Charger l'image du chemin
        self.road_image = pygame.image.load("assets/dalle.png").convert_alpha()
        self.road_image = pygame.transform.scale(self.road_image, (40, 40))

        # Gestion des vagues
        self.wave_number = 0
        self.max_waves = 3
        self.enemies_per_wave = 5
        self.wave_timer = 0
        self.spawned_enemies = 0
        self.enemy_speed = 2

        # État de jeu
        self.in_game_over_screen = False
        self.next_level_button_rect = None

        # Charger et jouer la musique
        pygame.mixer.music.load("assets/mario.mp3")  # Charger la musique
        pygame.mixer.music.set_volume(0.1)  # Ajuster le volume (0.0 à 1.0)
        pygame.mixer.music.play(-1, 0.0)  # Jouer la musique en boucle (-1 pour la boucle)

    def run(self):
        while self.running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if not self.in_game_over_screen:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        pos = pygame.mouse.get_pos()
                        tower_cost = 50
                        if self.money >= tower_cost:
                            self.towers.append(Tower(pos[0], pos[1]))
                            self.money -= tower_cost

                        if self.check_next_level_button(pos):
                            self.in_game_over_screen = False
                            self.start_new_level()
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.check_next_level_button(pygame.mouse.get_pos()):
                            self.in_game_over_screen = False
                            self.start_new_level()

            if not self.in_game_over_screen:
                self.update()
                self.draw()

            if self.castle_health <= 0:
                self.in_game_over_screen = True
                self.display_game_over("Game Over!")
                pygame.display.update()
                self.wait_for_restart()

            if self.wave_number >= self.max_waves and len(self.enemies) == 0 and self.castle_health > 0:
                self.in_game_over_screen = True
                self.display_game_over("Félicitations, vous avez gagné !")
                pygame.display.update()

    def update(self):
        if self.wave_number < self.max_waves:
            self.wave_timer += 1
            if self.wave_timer >= self.spawn_interval and self.spawned_enemies < self.enemies_per_wave:
                self.spawn_timer = 0
                self.spawn_enemy()

        for enemy in self.enemies:
            enemy.update()

        for enemy in self.enemies[:]:
            dx = enemy.pos[0] - WAYPOINTS[-1][0]
            dy = enemy.pos[1] - WAYPOINTS[-1][1]
            distance = (dx**2 + dy**2) ** 0.5

            if distance < 10:
                self.enemies.remove(enemy)
                self.castle_health -= 10

        for enemy in self.enemies[:]:
            if enemy.health <= 0:
                self.enemies.remove(enemy)
                self.money += 50

        for tower in self.towers:
            tower.update(self.enemies)

        if len(self.enemies) == 0 and self.spawned_enemies >= self.enemies_per_wave:
            self.wave_number += 1
            self.spawned_enemies = 0

    def draw(self):
        self.screen.fill((34, 139, 34))
        self.draw_path()

        castle_pos = WAYPOINTS[-1]
        castle_rect = self.castle_image.get_rect(center=castle_pos)
        self.screen.blit(self.castle_image, castle_rect)

        for tower in self.towers:
            tower.update(self.enemies)
            tower.draw(self.screen)

        for enemy in self.enemies:
            enemy.draw(self.screen)

        font = pygame.font.SysFont(None, 36)
        money_text = font.render(f"Argent: ${self.money}", True, (255, 255, 255))
        self.screen.blit(money_text, (10, 10))

        castle_text = font.render(f"Château: {self.castle_health} PV", True, (255, 255, 255))
        self.screen.blit(castle_text, (10, 50))

        wave_text = font.render(f"Vague: {self.wave_number}/{self.max_waves}", True, (255, 255, 255))
        self.screen.blit(wave_text, (10, 90))

        pygame.display.flip()

    def draw_path(self):
     for i in range(len(WAYPOINTS) - 1):
        start = WAYPOINTS[i]
        end = WAYPOINTS[i + 1]
        dx, dy = end[0] - start[0], end[1] - start[1]
        distance = math.hypot(dx, dy)

        if distance < 1:
            continue

        angle = math.atan2(dy, dx)
        steps = int(distance // 20)  # Moins d'espacement = route plus fluide

        for step in range(steps + 1):
            t = step / steps
            x = int(start[0] + dx * t)
            y = int(start[1] + dy * t)
            rotated_image = pygame.transform.rotate(self.road_image, -math.degrees(angle))
            rect = rotated_image.get_rect(center=(x, y))
            self.screen.blit(rotated_image, rect)



    def display_game_over(self, message="Game Over"):
        font = pygame.font.SysFont(None, 72)
        game_over_text = font.render(message, True, (255, 0, 0))
        restart_text = pygame.font.SysFont(None, 36).render("Appuyez sur R pour redémarrer", True, (255, 255, 255))

        self.screen.fill((0, 0, 0))
        self.screen.blit(game_over_text, (
            self.screen.get_width() // 2 - game_over_text.get_width() // 2,
            self.screen.get_height() // 2 - game_over_text.get_height() // 2
        ))
        self.screen.blit(restart_text, (
            self.screen.get_width() // 2 - restart_text.get_width() // 2,
            self.screen.get_height() // 2 + 50
        ))

        if message == "Félicitations, vous avez gagné !":
            self.display_next_level_button()

        pygame.display.flip()

    def wait_for_restart(self):
        waiting_for_restart = True
        while waiting_for_restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting_for_restart = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()
                        waiting_for_restart = False

    def reset_game(self):
        self.money = 100
        self.castle_health = 100
        self.towers = []
        self.enemies = []
        self.wave_number = 0
        self.spawned_enemies = 0
        self.wave_timer = 0
        self.in_game_over_screen = False
        self.next_level_button_rect = None

    def start_new_level(self):
        self.wave_number = 0
        self.spawned_enemies = 0
        self.enemies.clear()
        self.towers.clear()
        self.castle_health = 100
        self.money = 150
        self.max_waves += 1
        self.enemies_per_wave += 2
        self.enemy_speed += 0.5

    def display_next_level_button(self):
        font = pygame.font.SysFont(None, 48)
        next_level_text = font.render("Passer au niveau suivant", True, (255, 255, 255))
        self.next_level_button_rect = next_level_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 120))
        pygame.draw.rect(self.screen, (0, 0, 255), self.next_level_button_rect)
        self.screen.blit(next_level_text, self.next_level_button_rect.topleft)

    def check_next_level_button(self, pos):
        if self.next_level_button_rect:
            return self.next_level_button_rect.collidepoint(pos)
        return False

    def spawn_enemy(self):
        if self.wave_number < self.max_waves:
            spawn_offset = self.spawned_enemies * 60

            if self.wave_number == self.max_waves - 1 and self.spawned_enemies == self.enemies_per_wave - 1:
                enemy_type = "boss"
            elif self.wave_number % 2 == 1 and self.spawned_enemies == 0:
                enemy_type = "mini-boss"
            else:
                enemy_type = "normal"

            enemy = Enemy(enemy_type)
            enemy.pos = (WAYPOINTS[0][0] + spawn_offset, WAYPOINTS[0][1])
            enemy.speed = self.enemy_speed
            self.enemies.append(enemy)
            self.spawned_enemies += 1
