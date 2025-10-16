import pygame
import random
import math
import time

# Initialize Pygame
pygame.init()

# Display settings
WIDTH, HEIGHT = 1500, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enhanced 2 Player Tank Battle")

# Colors
WHITE = (255, 255, 255)
RED = (220, 20, 60)
BLUE = (30, 144, 255)
BLACK = (0, 0, 0)
GREEN = (50, 205, 50)
YELLOW = (255, 215, 0)
ORANGE = (255, 140, 0)
PURPLE = (148, 0, 211)
DARK_GREEN = (0, 100, 0)
DARK_GRAY = (70, 70, 70)
LIGHT_GRAY = (180, 180, 180)
BROWN = (139, 69, 19)
SAND = (238, 232, 170)

# Clock and FPS
clock = pygame.time.Clock()
FPS = 50

# Particle system for explosions
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-5, 5)
        self.color = color
        self.lifetime = random.randint(15, 30)
        self.size = random.randint(3, 8)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.3  # Gravity
        self.lifetime -= 1
        self.size = max(1, self.size - 0.2)
    
    def draw(self, win):
        if self.lifetime > 0:
            pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), int(self.size))

particles = []

# Obstacles with varied sizes
obstacles = []
for _ in range(5):
    width = random.choice([60, 80, 100])
    height = random.choice([40, 60, 80, 100])
    x = random.randint(150, WIDTH - 150)
    y = random.randint(100, HEIGHT - 100)
    obstacles.append(pygame.Rect(x, y, width, height))

# Enhanced Tank class with realistic physics
class Tank:
    def __init__(self, x, y, color, controls, name):
        self.x = x
        self.y = y
        self.angle = 0
        self.color = color
        self.controls = controls
        self.name = name
        
        # Physics properties
        self.velocity_x = 0
        self.velocity_y = 0
        self.max_speed = 4
        self.acceleration = 0.3
        self.friction = 0.92
        self.rotation_speed = 3.5
        
        # Combat properties
        self.bullets = []
        self.health = 100
        self.max_health = 100
        self.shoot_cooldown = 0
        self.max_cooldown = 15
        
        # Power-up effects
        self.speed_boost = 1.0
        self.damage_boost = 1.0
        self.shield_active = False
        self.rapid_fire = False
        self.power_up_timer = 0
        
        # Size
        self.width = 45
        self.height = 45
        
    def draw(self, win):
        # Draw tank body (rectangle)
        tank_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(tank_surface, self.color, (0, 0, self.width, self.height))
        pygame.draw.rect(tank_surface, BLACK, (0, 0, self.width, self.height), 2)
        
        # Draw turret
        turret_size = 25
        pygame.draw.circle(tank_surface, self.color, (self.width//2, self.height//2), turret_size//2)
        pygame.draw.circle(tank_surface, BLACK, (self.width//2, self.height//2), turret_size//2, 2)
        
        # Rotate tank
        rotated_tank = pygame.transform.rotate(tank_surface, self.angle)
        rect = rotated_tank.get_rect(center=(self.x, self.y))
        win.blit(rotated_tank, rect.topleft)
        
        # Draw barrel
        barrel_length = 50
        end_x = self.x + barrel_length * math.cos(math.radians(self.angle))
        end_y = self.y - barrel_length * math.sin(math.radians(self.angle))
        pygame.draw.line(win, BLACK, (self.x, self.y), (end_x, end_y), 6)
        
        # Draw shield effect
        if self.shield_active:
            pygame.draw.circle(win, (100, 200, 255), (int(self.x), int(self.y)), 40, 3)
        
        # Draw health bar background
        bar_width = 60
        bar_height = 8
        bar_x = self.x - bar_width // 2
        bar_y = self.y - 40
        pygame.draw.rect(win, BLACK, (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4))
        pygame.draw.rect(win, RED, (bar_x, bar_y, bar_width, bar_height))
        
        # Draw health bar foreground
        health_width = int(bar_width * (self.health / self.max_health))
        pygame.draw.rect(win, GREEN, (bar_x, bar_y, health_width, bar_height))
        
        # Draw tank name
        font_small = pygame.font.SysFont('arial', 16, bold=True)
        name_text = font_small.render(self.name, True, BLACK)
        win.blit(name_text, (self.x - name_text.get_width()//2, self.y - 55))
    
    def move(self, keys):
        # Smooth rotation
        if keys[self.controls['left']]:
            self.angle += self.rotation_speed
        if keys[self.controls['right']]:
            self.angle -= self.rotation_speed
        
        # Acceleration-based movement
        if keys[self.controls['up']]:
            self.velocity_x += self.acceleration * math.cos(math.radians(self.angle)) * self.speed_boost
            self.velocity_y -= self.acceleration * math.sin(math.radians(self.angle)) * self.speed_boost
        if keys[self.controls['down']]:
            self.velocity_x -= self.acceleration * math.cos(math.radians(self.angle)) * self.speed_boost * 0.4
            self.velocity_y += self.acceleration * math.sin(math.radians(self.angle)) * self.speed_boost * 0.4
        
        # Apply friction
        self.velocity_x *= self.friction
        self.velocity_y *= self.friction
        
        # Limit max speed
        speed = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
        if speed > self.max_speed * self.speed_boost:
            factor = (self.max_speed * self.speed_boost) / speed
            self.velocity_x *= factor
            self.velocity_y *= factor
        
        # Calculate new position
        temp_x = self.x + self.velocity_x
        temp_y = self.y + self.velocity_y
        
        # Collision detection
        tank_rect = pygame.Rect(temp_x - self.width//2, temp_y - self.height//2, self.width, self.height)
        
        # Check boundaries
        can_move = (self.width//2 <= temp_x <= WIDTH - self.width//2 and
                   self.height//2 <= temp_y <= HEIGHT - self.height//2)
        
        # Check obstacles
        if can_move:
            for ob in obstacles:
                if tank_rect.colliderect(ob):
                    can_move = False
                    # Bounce effect
                    self.velocity_x *= -0.3
                    self.velocity_y *= -0.3
                    break
        
        if can_move:
            self.x = temp_x
            self.y = temp_y
        else:
            # Stop movement if collision
            self.velocity_x *= 0.5
            self.velocity_y *= 0.5
    
    def shoot(self):
        if self.shoot_cooldown <= 0:
            bullet_speed = 12
            dx = bullet_speed * math.cos(math.radians(self.angle))
            dy = -bullet_speed * math.sin(math.radians(self.angle))
            
            # Spawn bullet slightly ahead of barrel
            spawn_offset = 40
            spawn_x = self.x + spawn_offset * math.cos(math.radians(self.angle))
            spawn_y = self.y - spawn_offset * math.sin(math.radians(self.angle))
            
            self.bullets.append({
                'x': spawn_x,
                'y': spawn_y,
                'dx': dx,
                'dy': dy,
                'damage': 10 * self.damage_boost,
                'lifetime': 120
            })
            
            # Set cooldown
            if self.rapid_fire:
                self.shoot_cooldown = self.max_cooldown // 2
            else:
                self.shoot_cooldown = self.max_cooldown
    
    def update_bullets(self, opponent):
        for bullet in self.bullets[:]:
            bullet['x'] += bullet['dx']
            bullet['y'] += bullet['dy']
            bullet['lifetime'] -= 1
            
            # Draw bullet with trail effect
            pygame.draw.circle(win, YELLOW, (int(bullet['x']), int(bullet['y'])), 6)
            pygame.draw.circle(win, ORANGE, (int(bullet['x']), int(bullet['y'])), 4)
            
            # Remove bullets that are out of bounds or expired
            if (bullet['x'] < 0 or bullet['x'] > WIDTH or 
                bullet['y'] < 0 or bullet['y'] > HEIGHT or 
                bullet['lifetime'] <= 0):
                self.bullets.remove(bullet)
                continue
            
            # Check collision with opponent
            distance = math.sqrt((opponent.x - bullet['x'])**2 + (opponent.y - bullet['y'])**2)
            if distance < 30:
                if opponent.shield_active:
                    opponent.shield_active = False
                    create_particles(int(bullet['x']), int(bullet['y']), (100, 200, 255), 15)
                else:
                    opponent.health -= bullet['damage']
                    create_particles(int(bullet['x']), int(bullet['y']), ORANGE, 20)
                self.bullets.remove(bullet)
                continue
            
            # Check collision with obstacles
            bullet_rect = pygame.Rect(bullet['x']-3, bullet['y']-3, 6, 6)
            for ob in obstacles:
                if bullet_rect.colliderect(ob):
                    create_particles(int(bullet['x']), int(bullet['y']), DARK_GRAY, 10)
                    self.bullets.remove(bullet)
                    break
    
    def update(self):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        
        # Update power-up timers
        if self.power_up_timer > 0:
            self.power_up_timer -= 1
            if self.power_up_timer == 0:
                self.speed_boost = 1.0
                self.damage_boost = 1.0
                self.shield_active = False
                self.rapid_fire = False

# Create explosion particles
def create_particles(x, y, color, count):
    for _ in range(count):
        particles.append(Particle(x, y, color))

# Power-up class with different types
class PowerUp:
    TYPES = {
        'health': {'color': GREEN, 'symbol': '+'},
        'speed': {'color': YELLOW, 'symbol': 'S'},
        'damage': {'color': RED, 'symbol': 'D'},
        'shield': {'color': (100, 200, 255), 'symbol': 'O'},
        'rapid': {'color': ORANGE, 'symbol': 'R'}
    }
    
    def __init__(self):
        self.type = random.choice(list(self.TYPES.keys()))
        self.size = 25
        self.rect = pygame.Rect(
            random.randint(100, WIDTH - 100),
            random.randint(100, HEIGHT - 100),
            self.size,
            self.size
        )
        self.active = True
        self.spawn_time = time.time()
        self.lifetime = 15  # seconds
        self.pulse = 0
    
    def draw(self):
        if self.active:
            # Pulsing effect
            self.pulse += 0.15
            pulse_size = int(self.size + math.sin(self.pulse) * 5)
            
            # Draw outer glow
            pygame.draw.circle(win, self.TYPES[self.type]['color'], 
                             self.rect.center, pulse_size, 3)
            
            # Draw power-up box
            pygame.draw.rect(win, self.TYPES[self.type]['color'], self.rect)
            pygame.draw.rect(win, BLACK, self.rect, 2)
            
            # Draw symbol
            font = pygame.font.SysFont('arial', 18, bold=True)
            symbol = font.render(self.TYPES[self.type]['symbol'], True, BLACK)
            symbol_rect = symbol.get_rect(center=self.rect.center)
            win.blit(symbol, symbol_rect)
            
            # Check if expired
            if time.time() - self.spawn_time > self.lifetime:
                self.active = False
    
    def check_collision(self, tank):
        if self.active:
            tank_rect = pygame.Rect(tank.x - tank.width//2, tank.y - tank.height//2, 
                                   tank.width, tank.height)
            if tank_rect.colliderect(self.rect):
                self.apply_effect(tank)
                self.active = False
                create_particles(self.rect.centerx, self.rect.centery, 
                               self.TYPES[self.type]['color'], 15)
    
    def apply_effect(self, tank):
        if self.type == 'health':
            tank.health = min(tank.max_health, tank.health + 30)
        elif self.type == 'speed':
            tank.speed_boost = 1.8
            tank.power_up_timer = 300  # 5 seconds
        elif self.type == 'damage':
            tank.damage_boost = 2.0
            tank.power_up_timer = 300
        elif self.type == 'shield':
            tank.shield_active = True
            tank.power_up_timer = 180  # 3 seconds
        elif self.type == 'rapid':
            tank.rapid_fire = True
            tank.power_up_timer = 240  # 4 seconds

# Tank setup
tank1 = Tank(150, HEIGHT // 2, RED, {
    'left': pygame.K_a,
    'right': pygame.K_d,
    'up': pygame.K_w,
    'down': pygame.K_s,
    'shoot': pygame.K_SPACE
}, "PLAYER 1")

tank2 = Tank(WIDTH - 150, HEIGHT // 2, BLUE, {
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT,
    'up': pygame.K_UP,
    'down': pygame.K_DOWN,
    'shoot': pygame.K_RETURN
}, "PLAYER 2")

# Power-ups list
powerups = []
powerup_spawn_timer = 0
powerup_spawn_interval = 180  # 3 seconds

# Fonts
font_large = pygame.font.SysFont('arial', 48, bold=True)
font_medium = pygame.font.SysFont('arial', 32, bold=True)
font_small = pygame.font.SysFont('arial', 20)

# Game state
game_over = False
winner = None

# Main game loop
running = True
while running:
    clock.tick(FPS)
    
    # Draw background
    win.fill(SAND)
    
    # Draw grid pattern
    for x in range(0, WIDTH, 50):
        pygame.draw.line(win, (220, 220, 190), (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT, 50):
        pygame.draw.line(win, (220, 220, 190), (0, y), (WIDTH, y), 1)
    
    keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if not game_over and event.type == pygame.KEYDOWN:
            if event.key == tank1.controls['shoot']:
                tank1.shoot()
            if event.key == tank2.controls['shoot']:
                tank2.shoot()
    
    if not game_over:
        # Update tanks
        tank1.move(keys)
        tank2.move(keys)
        tank1.update()
        tank2.update()
        
        # Update bullets
        tank1.update_bullets(tank2)
        tank2.update_bullets(tank1)
        
        # Spawn power-ups
        powerup_spawn_timer += 1
        if powerup_spawn_timer >= powerup_spawn_interval:
            if len(powerups) < 3:  # Max 3 power-ups at once
                powerups.append(PowerUp())
            powerup_spawn_timer = 0
        
        # Update and draw power-ups
        for powerup in powerups[:]:
            powerup.draw()
            powerup.check_collision(tank1)
            powerup.check_collision(tank2)
            if not powerup.active:
                powerups.remove(powerup)
        
        # Draw obstacles with 3D effect
        for ob in obstacles:
            pygame.draw.rect(win, BROWN, ob)
            pygame.draw.rect(win, DARK_GRAY, ob, 3)
            # Shadow effect
            shadow_rect = pygame.Rect(ob.x + 5, ob.y + 5, ob.width, ob.height)
            pygame.draw.rect(win, (0, 0, 0, 50), shadow_rect)
        
        # Draw tanks
        tank1.draw(win)
        tank2.draw(win)
        
        # Update and draw particles
        for particle in particles[:]:
            particle.update()
            if particle.lifetime > 0:
                particle.draw(win)
            else:
                particles.remove(particle)
        
        # Check win condition
        if tank1.health <= 0:
            game_over = True
            winner = "PLAYER 2"
            create_particles(int(tank1.x), int(tank1.y), RED, 50)
        elif tank2.health <= 0:
            game_over = True
            winner = "PLAYER 1"
            create_particles(int(tank2.x), int(tank2.y), BLUE, 50)
    
    else:
        # Game over screen
        # Draw semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        win.blit(overlay, (0, 0))
        
        # Draw winner text
        winner_text = font_large.render(f"{winner} WINS!", True, YELLOW)
        winner_rect = winner_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
        win.blit(winner_text, winner_rect)
        
        # Draw replay instruction
        replay_text = font_medium.render("Press R to Restart or Q to Quit", True, WHITE)
        replay_rect = replay_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
        win.blit(replay_text, replay_rect)
        
        # Handle restart
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            # Reset game
            tank1 = Tank(150, HEIGHT // 2, RED, {
                'left': pygame.K_a,
                'right': pygame.K_d,
                'up': pygame.K_w,
                'down': pygame.K_s,
                'shoot': pygame.K_SPACE
            }, "PLAYER 1")
            
            tank2 = Tank(WIDTH - 150, HEIGHT // 2, BLUE, {
                'left': pygame.K_LEFT,
                'right': pygame.K_RIGHT,
                'up': pygame.K_UP,
                'down': pygame.K_DOWN,
                'shoot': pygame.K_RETURN
            }, "PLAYER 2")
            
            powerups.clear()
            particles.clear()
            game_over = False
            winner = None
        
        if keys[pygame.K_q]:
            running = False
    
    # Draw FPS counter
    fps_text = font_small.render(f"FPS: {int(clock.get_fps())}", True, BLACK)
    win.blit(fps_text, (10, 10))
    
    pygame.display.update()

pygame.quit()
