import pygame
import random
import sys

# Initialize Pygame
pygame.init()


class Player:
    def __init__(self, screen_width, screen_height):
        self.width = 50
        self.height = 50
        self.x = screen_width // 2 - self.width // 2
        self.y = screen_height - self.height - 10
        self.speed = 5
        self.health = 5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, keys, screen_width, screen_height):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < screen_width - self.width:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.y > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < screen_height - self.height:
            self.rect.y += self.speed
        self.x = self.rect.x
        self.y = self.rect.y

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height))


class Bullet:
    def __init__(self, x, y):
        self.width = 5
        self.height = 10
        self.x = x - self.width // 2
        self.y = y
        self.speed = 7
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        self.rect.y -= self.speed
        self.y = self.rect.y
        self.x = self.rect.x


class BulletManager:
    def __init__(self):
        self.bullets = []

    def create_bullet(self, x, y):
        self.bullets.append(Bullet(x, y))

    def update_bullets(self, screen_height):
        # Move bullets and remove ones that are off screen
        self.bullets = [bullet for bullet in self.bullets if bullet.y > -bullet.height]
        for bullet in self.bullets:
            bullet.y -= bullet.speed

    def draw(self, screen):
        for bullet in self.bullets:
            pygame.draw.rect(screen, (255, 0, 0), (bullet.x, bullet.y, bullet.width, bullet.height))


class Enemy:
    def __init__(self, x, screen_width):
        self.width = 40
        self.height = 40
        self.x = x
        self.y = -self.height
        self.speed = 3
        self.direction = random.choice([-1, 1])
        self.movement_range = 100
        self.initial_x = x
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, screen_width):
        self.rect.y += self.speed
        # Sideways movement
        self.rect.x += self.direction * 2
        if abs(self.rect.x - self.initial_x) > self.movement_range:
            self.direction *= -1
        self.x = self.rect.x
        self.y = self.rect.y


class Boss:
    def __init__(self, x):
        self.width = 80
        self.height = 80
        self.x = x
        self.y = -self.height
        self.speed = 2
        self.health = 5
        self.direction = random.choice([-1, 1])
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, screen_width):
        self.rect.y += self.speed * 0.5
        self.rect.x += self.direction * self.speed
        if self.rect.left <= 0 or self.rect.right >= screen_width:
            self.direction *= -1
        self.x = self.rect.x
        self.y = self.rect.y


class GameManager:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Space Shooter")
        self.clock = pygame.time.Clock()

        # Game objects
        self.player = Player(screen_width, screen_height)
        self.bullet_manager = BulletManager()
        self.enemies = []
        self.bosses = []

        # Game state
        self.score = 0
        self.enemies_killed = 0
        self.bosses_killed = 0
        self.score_for_kill = 100
        self.score_for_boss_kill = 500

        # Timers
        self.enemy_timer = 0
        self.boss_timer = 0
        self.enemy_spawn_interval = 2000  # 2 seconds
        self.boss_spawn_interval = 10000  # 10 seconds

    def check_collision(self, rect1, rect2):
        return rect1.colliderect(rect2)

    def handle_collisions(self):
        # Check bullet collisions with enemies
        for bullet in self.bullet_manager.bullets[:]:
            for enemy in self.enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    if bullet in self.bullet_manager.bullets:
                        self.bullet_manager.bullets.remove(bullet)
                    if enemy in self.enemies:
                        self.enemies.remove(enemy)
                        self.score += self.score_for_kill
                        self.enemies_killed += 1

            # Check bullet collisions with bosses
            for boss in self.bosses[:]:
                if bullet.rect.colliderect(boss.rect):
                    if bullet in self.bullet_manager.bullets:
                        self.bullet_manager.bullets.remove(bullet)
                    boss.health -= 1
                    if boss.health <= 0:
                        self.bosses.remove(boss)
                        self.score += self.score_for_boss_kill
                        self.bosses_killed += 1


    def spawn_enemies(self):
        current_time = pygame.time.get_ticks()

        # Spawn regular enemies
        if current_time - self.enemy_timer >= self.enemy_spawn_interval:
            enemy_x = random.randint(0, self.screen_width - 40)
            self.enemies.append(Enemy(enemy_x, self.screen_width))
            self.enemy_timer = current_time

        # Spawn bosses
        if current_time - self.boss_timer >= self.boss_spawn_interval:
            boss_x = random.randint(0, self.screen_width - 80)
            self.bosses.append(Boss(boss_x))
            self.boss_timer = current_time

    def update_game_objects(self):
        keys = pygame.key.get_pressed()
        self.player.move(keys, self.screen_width, self.screen_height)
        self.bullet_manager.update_bullets(self.screen_height)

        # Update enemies
        for enemy in self.enemies[:]:
            enemy.move(self.screen_width)
            if enemy.y > self.screen_height:
                self.enemies.remove(enemy)

        # Update bosses
        for boss in self.bosses[:]:
            boss.move(self.screen_width)
            if boss.y > self.screen_height:
                self.bosses.remove(boss)

    def draw(self):
        self.screen.fill((0, 0, 0))  # Black background

        # Draw game objects
        self.player.draw(self.screen)
        self.bullet_manager.draw(self.screen)

        # Draw enemies
        for enemy in self.enemies:
            pygame.draw.rect(self.screen, (0, 255, 0), (enemy.x, enemy.y, enemy.width, enemy.height))

        # Draw bosses
        for boss in self.bosses:
            pygame.draw.rect(self.screen, (255, 0, 255), (boss.x, boss.y, boss.width, boss.height))

        # Draw score and stats
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        enemies_killed_text = font.render(f"Enemies: {self.enemies_killed}", True, (255, 255, 255))
        bosses_killed_text = font.render(f"Bosses: {self.bosses_killed}", True, (255, 255, 255))

        self.screen.blit(score_text, (10, 10))
        self.screen.blit(enemies_killed_text, (10, 50))
        self.screen.blit(bosses_killed_text, (10, 90))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.bullet_manager.create_bullet(
                            self.player.x + self.player.width // 2,
                            self.player.y
                        )

            # Game logic
            self.spawn_enemies()
            self.update_game_objects()
            self.handle_collisions()

            # Drawing
            self.draw()

            # Control game speed
            self.clock.tick(60)


def main():
    game = GameManager(800, 600)  # Create window of 800x600 pixels
    game.run()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
