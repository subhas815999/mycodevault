import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Display settings
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2 Player Tank Battle")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Obstacles
obstacles = [pygame.Rect(random.randint(150, 600), random.randint(100, 500), 50, 100) for _ in range(3)]

class Tank:
    def __init__(self, x, y, color, controls):
        self.x = x
        self.y = y
        self.angle = 0
        self.color = color
        self.controls = controls
        self.speed = 3
        self.bullets = []
        self.health = 100

    def draw(self, win):
        barrel_length = 40
        end_x = self.x + barrel_length * math.cos(math.radians(self.angle))
        end_y = self.y - barrel_length * math.sin(math.radians(self.angle))
        pygame.draw.rect(win, self.color, (self.x - 20, self.y - 20, 40, 40))
        pygame.draw.line(win, BLACK, (self.x, self.y), (end_x, end_y), 5)
        pygame.draw.rect(win, RED, (self.x - 25, self.y - 35, 50, 5))
        pygame.draw.rect(win, GREEN, (self.x - 25, self.y - 35, 50 * (self.health / 100), 5))

    def move(self, keys):
        temp_x, temp_y = self.x, self.y
        if keys[self.controls['left']]:
            self.angle += 3
        if keys[self.controls['right']]:
            self.angle -= 3
        if keys[self.controls['up']]:
            temp_x += self.speed * math.cos(math.radians(self.angle))
            temp_y -= self.speed * math.sin(math.radians(self.angle))
        if keys[self.controls['down']]:
            temp_x -= self.speed * math.cos(math.radians(self.angle))
            temp_y += self.speed * math.sin(math.radians(self.angle))

        tank_rect = pygame.Rect(temp_x - 20, temp_y - 20, 40, 40)
        if (0 <= tank_rect.left and tank_rect.right <= WIDTH and
            0 <= tank_rect.top and tank_rect.bottom <= HEIGHT and
            not any(tank_rect.colliderect(ob) for ob in obstacles)):
            self.x, self.y = temp_x, temp_y

    def shoot(self):
        dx = 10 * math.cos(math.radians(self.angle))
        dy = -10 * math.sin(math.radians(self.angle))
        self.bullets.append([self.x, self.y, dx, dy])

    def update_bullets(self, opponent):
        for bullet in self.bullets[:]:
            bullet[0] += bullet[2]
            bullet[1] += bullet[3]
            pygame.draw.circle(win, BLACK, (int(bullet[0]), int(bullet[1])), 5)
            if (opponent.x - 20 < bullet[0] < opponent.x + 20 and
                opponent.y - 20 < bullet[1] < opponent.y + 20):
                opponent.health -= 10
                show_explosion(int(bullet[0]), int(bullet[1]))
                self.bullets.remove(bullet)
            else:
                bullet_rect = pygame.Rect(bullet[0]-2, bullet[1]-2, 4, 4)
                if any(bullet_rect.colliderect(ob) for ob in obstacles):
                    self.bullets.remove(bullet)

# Explosion animation
def show_explosion(x, y):
    for i in range(6):
        pygame.draw.circle(win, YELLOW, (x, y), 15 + i, 1)

# Power-up class
class PowerUp:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100), 20, 20)
        self.active = True

    def draw(self):
        if self.active:
            pygame.draw.rect(win, GREEN, self.rect)

    def check_collision(self, tank):
        if self.active and pygame.Rect(tank.x - 20, tank.y - 20, 40, 40).colliderect(self.rect):
            tank.health = min(100, tank.health + 20)
            self.active = False

# Tank setup
tank1 = Tank(100, HEIGHT // 2, RED, {'left': pygame.K_a, 'right': pygame.K_d, 'up': pygame.K_w, 'down': pygame.K_s, 'shoot': pygame.K_SPACE})
tank2 = Tank(WIDTH - 100, HEIGHT // 2, BLUE, {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'up': pygame.K_UP, 'down': pygame.K_DOWN, 'shoot': pygame.K_RETURN})

# Font and power-up
font = pygame.font.SysFont(None, 36)
powerup = PowerUp()

# Game loop
running = True
while running:
    clock.tick(FPS)
    win.fill(WHITE)

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == tank1.controls['shoot']:
                tank1.shoot()
            if event.key == tank2.controls['shoot']:
                tank2.shoot()

    tank1.move(keys)
    tank2.move(keys)

    tank1.update_bullets(tank2)
    tank2.update_bullets(tank1)

    for ob in obstacles:
        pygame.draw.rect(win, BLACK, ob)

    tank1.draw(win)
    tank2.draw(win)

    powerup.draw()
    powerup.check_collision(tank1)
    powerup.check_collision(tank2)

    if tank1.health <= 0 or tank2.health <= 0:
        winner = "Blue" if tank1.health <= 0 else "Red"
        text = font.render(f"{winner} Wins!", True, BLACK)
        win.blit(text, (WIDTH // 2 - 80, HEIGHT // 2))
        pygame.display.update()
        pygame.time.delay(3000)
        running = False
        continue

    pygame.display.update()

pygame.quit()
