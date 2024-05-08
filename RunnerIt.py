import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen setup
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Endless Runner')

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Player setup
player_size = 50
player_x = 100
player_y = screen_height - player_size
player = pygame.Rect(player_x, player_y, player_size, player_size)

# Obstacle setup
obstacle_width = 20
obstacle_height = random.randint(20, 100)
obstacle_x = screen_width - obstacle_width
obstacle_y = screen_height - obstacle_height
obstacle_speed = 10
obstacles = []

# Game variables
gravity = 0.6
player_jump = -12
player_velocity = 0
game_speed = 7  # Slowed down obstacles
score = 0
lives = 3
jump_count = 0  # Track the number of jumps
max_jumps = 2  # Maximum number of jumps allowed (double jump)

# Font setup
font = pygame.font.Font(None, 36)

def draw_objects():
    screen.fill(black)
    pygame.draw.rect(screen, white, player)
    for obstacle in obstacles:
        pygame.draw.rect(screen, red, obstacle)
    score_text = font.render(f"Score: {score}", True, white)
    lives_text = font.render(f"Lives: {lives}", True, white)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))

def add_obstacle():
    height = random.randint(20, 100)
    obstacles.append(pygame.Rect(screen_width, screen_height - height, obstacle_width, height))

def update_obstacles():
    global score
    for obstacle in obstacles:
        obstacle.x -= game_speed
        if obstacle.x < -obstacle_width:
            obstacles.remove(obstacle)
            score += 1

def check_collisions():
    for obstacle in obstacles:
        if player.colliderect(obstacle):
            return True
    return False

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if jump_count < max_jumps:
                    player_velocity = player_jump
                    jump_count += 1

    # Player physics
    player_velocity += gravity
    player.y += player_velocity
    if player.bottom > screen_height:
        player.bottom = screen_height
        jump_count = 0  # Reset jump count when player touches the ground

    # Obstacle management
    if not obstacles or obstacles[-1].x < screen_width - 300:
        add_obstacle()
    update_obstacles()

    # Check for collisions
    if check_collisions():
        lives -= 1
        player.x = 100
        player.y = screen_height - player_size
        player_velocity = 0
        jump_count = 0  # Reset jump count on collision
        if lives == 0:
            running = False
        else:
            obstacles.clear()

    # Drawing
    draw_objects()

    pygame.display.flip()

    # Frame rate
    pygame.time.Clock().tick(30)

pygame.quit()
sys.exit()