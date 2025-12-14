import pygame
import random
import math

# Initialize pygame
pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Load images
player_img = pygame.image.load("player.png")
player_img = pygame.transform.scale(player_img, (64, 64))

enemy_img = pygame.image.load("enemy.png")
enemy_img = pygame.transform.scale(enemy_img, (64, 64))

boss_img = pygame.image.load("boss.png")
boss_img = pygame.transform.scale(boss_img, (128, 128))

bullet_img = pygame.image.load("bullet.png")
bullet_img = pygame.transform.scale(bullet_img, (16, 32))

background_img = pygame.image.load("background.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Player
player_x = 370
player_y = 500
player_speed = 5

# Bullet
bullet_speed = 10
bullets = []

# Enemies
enemy_speed = 2
num_enemies = 5
enemies = []

for _ in range(num_enemies):
    enemy = {
        "x": random.randint(0, WIDTH - 64),
        "y": random.randint(50, 150),
        "health": 3,
        "max_health": 3,
        "speed": enemy_speed
    }
    enemies.append(enemy)

# Boss
boss = {
    "x": WIDTH//2 - 64,
    "y": 50,
    "health": 20,
    "max_health": 20,
    "speed": 1.5,
    "alive": True
}

# Score & font
score = 0
font = pygame.font.Font(None, 36)

# Game over
game_over = False

# Functions
def show_score():
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

def fire_bullet(x, y):
    bullets.append({"x": x + 24, "y": y})

def collision(enemy, bullet):
    distance = math.sqrt((enemy["x"] - bullet["x"])**2 + (enemy["y"] - bullet["y"])**2)
    return distance < 35

def draw_player(x, y):
    screen.blit(player_img, (x, y))

def draw_enemy(enemy):
    screen.blit(enemy_img, (enemy["x"], enemy["y"]))
    health_ratio = enemy["health"] / enemy["max_health"]
    pygame.draw.rect(screen, (255,0,0), (enemy["x"], enemy["y"] - 10, 64, 5))
    pygame.draw.rect(screen, (0,255,0), (enemy["x"], enemy["y"] - 10, 64 * health_ratio, 5))

def draw_boss(boss):
    if boss["alive"]:
        screen.blit(boss_img, (boss["x"], boss["y"]))
        health_ratio = boss["health"] / boss["max_health"]
        pygame.draw.rect(screen, (255,0,0), (boss["x"], boss["y"] - 15, 128, 10))
        pygame.draw.rect(screen, (0,255,0), (boss["x"], boss["y"] - 15, 128 * health_ratio, 10))

# Clock
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    screen.blit(background_img, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - 64:
            player_x += player_speed
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed
        if keys[pygame.K_DOWN] and player_y < HEIGHT - 64:
            player_y += player_speed
        if keys[pygame.K_SPACE]:
            if len(bullets) < 5:
                fire_bullet(player_x, player_y)

        # Update bullets
        for bullet in bullets[:]:
            bullet["y"] -= bullet_speed
            screen.blit(bullet_img, (bullet["x"], bullet["y"]))
            if bullet["y"] <= 0:
                bullets.remove(bullet)

        # Update enemies
        for enemy in enemies:
            enemy["x"] += enemy["speed"]
            if enemy["x"] <= 0 or enemy["x"] >= WIDTH - 64:
                enemy["speed"] *= -1
                enemy["y"] += 30

            # Collision with bullets
            for bullet in bullets[:]:
                if collision(enemy, bullet):
                    enemy["health"] -= 1
                    bullets.remove(bullet)
                    if enemy["health"] <= 0:
                        score += 1
                        enemy["x"] = random.randint(0, WIDTH - 64)
                        enemy["y"] = random.randint(50, 150)
                        enemy["health"] = enemy["max_health"]

            # Collision with player
            distance_to_player = math.sqrt((enemy["x"] - player_x)**2 + (enemy["y"] - player_y)**2)
            if distance_to_player < 50:
                game_over = True

            draw_enemy(enemy)

        # Update boss
        if boss["alive"]:
            boss["x"] += boss["speed"]
            if boss["x"] <= 0 or boss["x"] >= WIDTH - 128:
                boss["speed"] *= -1
            # Bullet collision
            for bullet in bullets[:]:
                if collision(boss, bullet):
                    boss["health"] -= 1
                    bullets.remove(bullet)
                    if boss["health"] <= 0:
                        boss["alive"] = False
                        score += 10
            # Player collision
            distance_to_player = math.sqrt((boss["x"] - player_x)**2 + (boss["y"] - player_y)**2)
            if distance_to_player < 70:
                game_over = True

            draw_boss(boss)

        draw_player(player_x, player_y)
        show_score()
    else:
        # Game over screen
        screen.fill((0, 0, 0))
        game_over_text = font.render("GAME OVER!", True, (255, 0, 0))
        final_score_text = font.render(f"Your Final Score: {score}", True, (255, 255, 255))
        restart_text = font.render("Press R to Restart", True, (255, 255, 0))

        # Center texts
        screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 50))
        screen.blit(final_score_text, (WIDTH//2 - final_score_text.get_width()//2, HEIGHT//2))
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 50))

        # Restart game
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            player_x, player_y = 370, 500
            bullets.clear()
            enemies.clear()
            for _ in range(num_enemies):
                enemy = {
                    "x": random.randint(0, WIDTH - 64),
                    "y": random.randint(50, 150),
                    "health": 3,
                    "max_health": 3,
                    "speed": enemy_speed
                }
                enemies.append(enemy)
            boss["health"] = boss["max_health"]
            boss["alive"] = True
            score = 0
            game_over = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()
