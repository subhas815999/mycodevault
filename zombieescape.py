import pygame
import sys
import random

pygame.init()

# Display setup
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 40
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Split – Ultimate Pixel Edition")

# Colors
SURVIVOR_COLOR = (50, 200, 50)
ZOMBIE_COLOR = (200, 50, 50)
WALL_COLOR = (100, 0, 200)
WALL_OUTLINE = (0, 0, 0)
FLOOR_COLOR = (20, 20, 20)
POWERUP_COLOR = (255, 215, 0)
TEXT_COLOR = (255, 255, 255)
CLOAK_COLOR = (0, 0, 0)
FLASH_COLOR = (255, 255, 0)

font = pygame.font.SysFont(None, 32)
clock = pygame.time.Clock()

cols = WIDTH // TILE_SIZE
rows = HEIGHT // TILE_SIZE

# Game states
menu_active = True
control_screen = False
round_over = False
selected = {"left": None, "right": None}

# Gameplay variables
maze = []
survivor = zombie = None
powerups = []
cloak = False
cloak_timer = 0
cloak_cooldown = 0
infected = False
game_timer = 90
start_ticks = 0
survivor_speed = 4
zombie_speed = 3
stun_timer = 0
step_survivor = step_zombie = 0
round_end_time = 0

# -------------------------------------------------
# Functions
# -------------------------------------------------
def generate_maze():
    """Generate a random maze with walls and empty spaces."""
    maze = []
    for y in range(rows):
        row = []
        for x in range(cols):
            row.append(1 if random.random() < 0.22 else 0)
        maze.append(row)
    # Ensure start and end are empty
    maze[1][1] = 0
    maze[rows - 2][cols - 2] = 0
    return maze

def spawn_powerups(maze, count):
    """Spawn collectible powerups in empty spaces."""
    items = []
    for _ in range(count):
        while True:
            x = random.randint(1, cols - 2)
            y = random.randint(1, rows - 2)
            if maze[y][x] == 0:
                items.append(pygame.Rect(x * TILE_SIZE + 10, y * TILE_SIZE + 10, 20, 20))
                break
    return items

def draw_pixel_char(rect, base_color, step, flash=False, cloak=False):
    """Draws a simple animated pixel character."""
    x, y = rect.topleft
    color = FLASH_COLOR if flash else base_color
    if cloak:
        color = CLOAK_COLOR
    leg_offset = 3 if step % 20 < 10 else -3
    arm_offset = -leg_offset
    pygame.draw.rect(screen, color, (x + 10, y - 5, 16, 16))               # Head
    pygame.draw.rect(screen, color, (x + 8, y + 12, 24, 18))               # Body
    pygame.draw.rect(screen, color, (x - 4, y + 12 + arm_offset, 10, 6))   # Left Arm
    pygame.draw.rect(screen, color, (x + 24, y + 12 - arm_offset, 10, 6))  # Right Arm
    pygame.draw.rect(screen, color, (x + 10, y + 30 + leg_offset, 8, 14))  # Left Leg
    pygame.draw.rect(screen, color, (x + 20, y + 30 - leg_offset, 8, 14))  # Right Leg

def draw_wall(x, y):
    rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, WALL_COLOR, rect)
    pygame.draw.rect(screen, WALL_OUTLINE, rect, 2)
    pygame.draw.line(screen, (150, 0, 255), rect.topleft, rect.bottomright, 1)
    pygame.draw.line(screen, (150, 0, 255), rect.topright, rect.bottomleft, 1)

def draw_fog():
    fog = pygame.Surface((WIDTH, HEIGHT))
    fog.set_alpha(50)
    fog.fill((0, 0, 0))
    screen.blit(fog, (0, 0))

def draw_menu():
    screen.fill((25, 25, 25))
    title = font.render("Zombie Split", True, TEXT_COLOR)
    left = font.render("← LEFT: Zombie", True, ZOMBIE_COLOR)
    right = font.render("→ RIGHT: Survivor", True, SURVIVOR_COLOR)
    info = font.render("Press SPACE to continue", True, TEXT_COLOR)
    screen.blit(title, (WIDTH // 2 - 80, HEIGHT // 4))
    screen.blit(left, (WIDTH // 4 - 80, HEIGHT // 2))
    screen.blit(right, (3 * WIDTH // 4 - 80, HEIGHT // 2))
    screen.blit(info, (WIDTH // 2 - 130, 3 * HEIGHT // 4))

def draw_controls():
    screen.fill((15, 15, 15))
    title = font.render("Controls", True, TEXT_COLOR)
    left_controls = [
        "Zombie – Arrow Keys to move",
        "Avoid the survivor's flash!"
    ]
    right_controls = [
        "Survivor – W/A/S/D to move",
        "SPACE to activate cloak",
        "F to flash if close to zombie"
    ]
    screen.blit(title, (WIDTH // 2 - 50, 40))
    for i, line in enumerate(left_controls):
        txt = font.render(line, True, ZOMBIE_COLOR)
        screen.blit(txt, (100, 100 + i * 40))
    for i, line in enumerate(right_controls):
        txt = font.render(line, True, SURVIVOR_COLOR)
        screen.blit(txt, (WIDTH // 2 + 20, 100 + i * 40))
    info = font.render("Press SPACE to Start Game", True, TEXT_COLOR)
    screen.blit(info, (WIDTH // 2 - 130, HEIGHT - 60))

def reset_game():
    global maze, survivor, zombie, powerups
    global cloak, cloak_timer, cloak_cooldown
    global infected, game_timer, start_ticks, round_over, round_end_time
    global survivor_speed, zombie_speed, stun_timer
    global step_survivor, step_zombie

    maze = generate_maze()
    survivor = pygame.Rect(50, 50, TILE_SIZE - 6, TILE_SIZE - 6)
    zombie = pygame.Rect(WIDTH - 90, HEIGHT - 90, TILE_SIZE - 6, TILE_SIZE - 6)
    powerups = spawn_powerups(maze, 6)
    survivor_speed = 4
    zombie_speed = 3
    cloak = False
    cloak_timer = 0
    cloak_cooldown = 0
    infected = False
    stun_timer = 0
    game_timer = 90
    start_ticks = pygame.time.get_ticks()
    round_over = False
    round_end_time = 0
    step_survivor = step_zombie = 0

def can_move(rect, maze):
    """Check if a character can move into the given position without hitting walls."""
    for px, py in [(rect.left, rect.top), (rect.right - 1, rect.top),
                   (rect.left, rect.bottom - 1), (rect.right - 1, rect.bottom - 1)]:
        gx, gy = px // TILE_SIZE, py // TILE_SIZE
        if 0 <= gx < cols and 0 <= gy < rows:
            if maze[gy][gx] == 1:
                return False
    return True

def move(rect, up, down, left, right, speed):
    new = rect.copy()
    keys = pygame.key.get_pressed()
    if keys[up]: new.y -= speed
    if keys[down]: new.y += speed
    if keys[left]: new.x -= speed
    if keys[right]: new.x += speed
    if can_move(new, maze):
        rect.x, rect.y = new.x, new.y

# Initialize game
reset_game()

# -------------------------------------------------
# Main loop
# -------------------------------------------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # ------------------- MENU -------------------
    if menu_active:
        draw_menu()
        if keys[pygame.K_LEFT]: selected["left"] = "Zombie"
        if keys[pygame.K_RIGHT]: selected["right"] = "Survivor"
        if keys[pygame.K_SPACE] and selected["left"] and selected["right"]:
            menu_active = False
            control_screen = True
        pygame.display.flip()
        continue

    # ------------------- CONTROLS -------------------
    if control_screen:
        draw_controls()
        if keys[pygame.K_SPACE]:
            control_screen = False
            reset_game()
        pygame.display.flip()
        continue

    # ------------------- ROUND OVER -------------------
    if round_over:
        screen.fill(FLOOR_COLOR)
        msg = "🧟 Zombie Wins by Infection!" if infected else "🧍 Survivor Escaped!"
        end_text = font.render(msg, True, TEXT_COLOR)
        screen.blit(end_text, (WIDTH // 2 - 160, HEIGHT // 2))
        pygame.display.flip()

        if round_end_time == 0:
            round_end_time = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - round_end_time > 3500:
            reset_game()
        continue

    # ------------------- GAMEPLAY -------------------
    screen.fill(FLOOR_COLOR)

    # Handle cloak
    if cloak_timer > 0:
        cloak = True
        cloak_timer -= 1
    else:
        cloak = False

    if cloak_cooldown > 0:
        cloak_cooldown -= 1

    if keys[pygame.K_SPACE] and not cloak and cloak_timer == 0 and cloak_cooldown == 0:
        cloak_timer = 100  # ~1.5 sec
        cloak_cooldown = 180  # ~3 sec cooldown

    # Flash stun: works in radius
    if keys[pygame.K_f] and stun_timer == 0:
        flash_rect = survivor.inflate(60, 60)
        if flash_rect.colliderect(zombie):
            stun_timer = 60  # 1 second
            print("Zombie stunned!")

    # Move survivor
    move(survivor, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, survivor_speed)
    if any(keys[k] for k in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]):
        step_survivor += 1

    # Move zombie (if not stunned)
    if stun_timer == 0:
        move(zombie, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, zombie_speed)
        if any(keys[k] for k in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]):
            step_zombie += 1

    # Countdown stun timer
    if stun_timer > 0:
        stun_timer -= 1

    # Powerups
    for p in powerups[:]:
        if survivor.colliderect(p):
            survivor_speed += 1
            powerups.remove(p)

    # Collision check
    if zombie.colliderect(survivor) and not cloak:
        infected = True
        round_over = True

    # Timer
    seconds = (pygame.time.get_ticks() - start_ticks) // 1000
    remaining = max(0, game_timer - seconds)
    if remaining == 0 and not infected:
        round_over = True

    # Draw fog and maze
    draw_fog()
    for y in range(rows):
        for x in range(cols):
            if maze[y][x] == 1:
                draw_wall(x, y)

    # Draw characters
    draw_pixel_char(survivor, SURVIVOR_COLOR, step_survivor, flash=(stun_timer > 0), cloak=cloak)
    draw_pixel_char(zombie, ZOMBIE_COLOR, step_zombie, flash=(stun_timer > 0))

    # Draw powerups
    for p in powerups:
        pygame.draw.rect(screen, POWERUP_COLOR, p)

    # Draw timer
    timer_text = font.render(f"Time Left: {remaining}s", True, TEXT_COLOR)
    screen.blit(timer_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)
