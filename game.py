import pygame
import math
import os
from enemy import Enemy
from map import WAYPOINTS
from tower import Tower

HIGHSCORE_FILE = "highscores.txt"

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()
        self.money = 150
        self.max_towers = 5
        self.towers = []
        self.enemies = []
        self.spawn_timer = 0
        self.spawn_interval = 120
        self.castle_health = 100
        self.castle_image = pygame.image.load("assets/chateau.png").convert_alpha()
        self.castle_image = pygame.transform.scale(self.castle_image, (60, 60))

        self.road_image = pygame.image.load("assets/dalle.png").convert_alpha()
        self.road_image = pygame.transform.scale(self.road_image, (40, 40))

        self.wave_number = 0
        self.max_waves = 3
        self.enemies_per_wave = 6
        self.wave_timer = 0
        self.spawned_enemies = 0
        self.enemy_speed = 3

        self.last_spawn_time = pygame.time.get_ticks()
        self.spawn_delay = 200

        self.score = 0
        self.in_game_over_screen = False
        self.next_level_button_rect = None

        self.warning_message = ""
        self.warning_start_time = 0
        self.warning_duration = 3000

        self.lives = 3

        self.heart_image = pygame.image.load("assets/coeur.png").convert_alpha()
        self.heart_image = pygame.transform.scale(self.heart_image, (20, 20))

        pygame.mixer.music.load("assets/mario.mp3")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1, 0.0)

        self.level = 1

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
                        if self.money >= tower_cost and len(self.towers) < self.max_towers:
                            self.towers.append(Tower(pos[0], pos[1]))
                            self.money -= tower_cost
                        elif len(self.towers) >= self.max_towers:
                            print("Limite de tours atteinte !")

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
                self.lives -= 1
                self.in_game_over_screen = True
                self.save_score(self.score)
                self.display_game_over("Game Over!")
                pygame.display.update()
                self.wait_for_restart()

            if self.wave_number >= self.max_waves and len(self.enemies) == 0 and self.castle_health > 0:
                self.in_game_over_screen = True
                self.save_score(self.score)
                if self.level >= 10:
                    self.display_game_over("Félicitations, vous avez terminé le jeu !")
                else:
                    self.display_game_over("Félicitations, vous avez gagné !")
                pygame.display.update()

    def update(self):
        if self.wave_number < self.max_waves and self.spawned_enemies < self.enemies_per_wave:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_spawn_time >= self.spawn_delay:
                self.spawn_enemy()
                self.last_spawn_time = current_time

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
                self.score += 10

        for tower in self.towers:
            tower.update(self.enemies)

        if len(self.enemies) == 0 and self.spawned_enemies >= self.enemies_per_wave:
            self.wave_number += 1
            self.spawned_enemies = 0

            if self.wave_number == self.max_waves - 1:
                self.warning_message = "⚠️ Un puissant boss approche ! ⚠️"
                self.warning_start_time = pygame.time.get_ticks()

        if self.wave_number > self.max_waves:
            self.wave_number = self.max_waves

    def draw(self):
        self.screen.fill((34, 139, 34))
        self.draw_path()

        castle_pos = WAYPOINTS[-1]
        castle_rect = self.castle_image.get_rect(center=castle_pos)
        self.screen.blit(self.castle_image, castle_rect)

        font = pygame.font.SysFont(None, 28)
        health_text = font.render(f"{self.castle_health} PV", True, (255, 0, 0))
        text_rect = health_text.get_rect(center=(castle_rect.centerx, castle_rect.top - 10))
        self.screen.blit(health_text, text_rect)

        for tower in self.towers:
            tower.update(self.enemies)
            tower.draw(self.screen)

        for enemy in self.enemies:
            enemy.draw(self.screen)

        font = pygame.font.SysFont(None, 28)
        self.screen.blit(font.render(f"Argent: ${self.money}", True, (255, 255, 255)), (10, 10))
        self.screen.blit(font.render(f"Vague: {min(self.wave_number + 1, self.max_waves)}/{self.max_waves}", True, (255, 255, 255)), (10, 50))
        self.screen.blit(font.render(f"Tours : {len(self.towers)} / {self.max_towers}", True, (255, 255, 255)), (10, 90))
        self.screen.blit(font.render(f"Niveau : {self.level}/10", True, (255, 255, 255)), (10, 130))

        for i in range(self.lives):
            x = self.screen.get_width() // 2 - (self.lives * 20) // 2 + i * 35
            y = 10
            self.screen.blit(self.heart_image, (x, y))

        if self.warning_message:
            current_time = pygame.time.get_ticks()
            if current_time - self.warning_start_time < self.warning_duration:
                font = pygame.font.SysFont(None, 48)
                warning_text = font.render(self.warning_message, True, (255, 0, 0))
                self.screen.blit(warning_text, (
                    self.screen.get_width() // 2 - warning_text.get_width() // 2,
                    self.screen.get_height() // 2 - 100))
            else:
                self.warning_message = ""

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
            steps = int(distance // 20)
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
        text_y = self.screen.get_height() // 2 - game_over_text.get_height() // 2 - 100
        self.screen.blit(game_over_text, (self.screen.get_width() // 2 - game_over_text.get_width() // 2, text_y))
        self.screen.blit(restart_text, (self.screen.get_width() // 2 - restart_text.get_width() // 2, text_y + 100))

        if message == "Félicitations, vous avez gagné !" or message == "Félicitations, vous avez terminé le jeu !":
            self.display_next_level_button()

        self.display_highscores()
        pygame.display.flip()

    def display_highscores(self):
        if not os.path.exists(HIGHSCORE_FILE):
            return
        try:
            with open(HIGHSCORE_FILE, "r") as f:
                scores = [int(line.strip()) for line in f if line.strip().isdigit()]
        except:
            scores = []

        top_scores = sorted(scores, reverse=True)[:5]
        font = pygame.font.SysFont(None, 26)
        self.screen.blit(font.render("Top Scores:", True, (255, 255, 0)), (50, 300))
        for i, score in enumerate(top_scores):
            text = font.render(f"{i+1}. {score}", True, (255, 255, 255))
            self.screen.blit(text, (50, 340 + i * 30))

    def wait_for_restart(self):
        waiting_for_restart = True
        while waiting_for_restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting_for_restart = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        if self.lives > 0:
                            self.reset_game()
                        else:
                            print("Plus de vies. Partie terminée.")
                            self.running = False
                        waiting_for_restart = False

    def reset_game(self):
        self.money = 250
        self.castle_health = 100
        self.towers = []
        self.enemies = []
        self.wave_number = 0
        self.spawned_enemies = 0
        self.wave_timer = 0
        self.in_game_over_screen = False
        self.next_level_button_rect = None
        self.score = 0
        self.level = 1

    def start_new_level(self):
        if self.level < 10:
            self.level += 1
            self.wave_number = 0
            self.spawned_enemies = 0
            self.enemies.clear()
            self.towers.clear()
            self.castle_health = 100
            self.money = 200
            self.max_waves += 0
            self.enemies_per_wave += 2
            self.enemy_speed += 0.1
            self.max_towers += 1
            self.castle_health += 10
        else:
            self.in_game_over_screen = True
            self.save_score(self.score)
            self.display_game_over("Félicitations, vous avez terminé le jeu !")

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
        if self.spawned_enemies < self.enemies_per_wave:
            if self.wave_number == self.max_waves - 1:
                if self.spawned_enemies == self.enemies_per_wave - 1:
                    enemy = Enemy(enemy_type="boss", speed=self.enemy_speed)
                else:
                    enemy = Enemy(enemy_type="normal", speed=self.enemy_speed)
            elif self.wave_number == self.max_waves - 2:
                if self.spawned_enemies == self.enemies_per_wave - 1:
                    enemy = Enemy(enemy_type="mini-boss", speed=self.enemy_speed)
                else:
                    enemy = Enemy(enemy_type="normal", speed=self.enemy_speed)
            else:
                enemy = Enemy(enemy_type="normal", speed=self.enemy_speed)

            self.enemies.append(enemy)
            self.spawned_enemies += 1
            self.spawn_delay = 500

    def save_score(self, score):
        try:
            with open(HIGHSCORE_FILE, "a") as f:
                f.write(str(score) + "\n")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du score : {e}")
