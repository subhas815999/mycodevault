import pygame
import random
import math
import time
import sys

# Ultra-Realistic Two-Player Street Fighting Game
# Features: Pixelated graphics, realistic physics, random power-ups, intense combat

class Fighter:
    def __init__(self, x, y, controls, color):
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.width = 40
        self.height = 60
        self.color = color
        self.controls = controls

        # Ultra-realistic physics properties
        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration = 0.8
        self.friction = 0.85
        self.max_speed = 8
        self.jump_power = -18
        self.gravity = 0.8
        self.on_ground = False
        self.air_resistance = 0.98

        # Combat properties
        self.health = 100
        self.max_health = 100
        self.attack_damage = 20
        self.attack_range = 45
        self.attack_cooldown = 0
        self.attack_cooldown_max = 20
        self.is_attacking = False
        self.hit_cooldown = 0
        self.combo_count = 0
        self.last_hit_time = 0

        # Animation states for ultra-realistic movement
        self.animation_state = "idle"
        self.animation_frame = 0
        self.animation_timer = 0
        self.facing_right = True
        self.movement_trail = []

        # Power-up effects system
        self.power_effects = {}
        self.power_duration = {}
        self.power_particles = []

        # Combat effects for realism
        self.knockback_x = 0
        self.knockback_y = 0
        self.stun_timer = 0
        self.screen_shake = 0
        self.damage_numbers = []

        # Advanced movement mechanics
        self.dash_cooldown = 0
        self.dash_power = 15
        self.wall_jump_available = True

    def handle_input(self, keys):
        if self.stun_timer > 0:
            return

        # Advanced movement with momentum conservation
        if keys[self.controls['left']]:
            self.velocity_x -= self.acceleration
            self.facing_right = False
            if self.on_ground and self.animation_state != "attacking":
                self.animation_state = "running"
        elif keys[self.controls['right']]:
            self.velocity_x += self.acceleration
            self.facing_right = True
            if self.on_ground and self.animation_state != "attacking":
                self.animation_state = "running"
        else:
            if self.on_ground and self.animation_state != "attacking":
                self.animation_state = "idle"

        # Realistic jumping with air control
        if keys[self.controls['jump']]:
            if self.on_ground:
                self.velocity_y = self.jump_power
                self.on_ground = False
                self.animation_state = "jumping"
                self.wall_jump_available = True
            elif self.wall_jump_available and abs(self.velocity_x) > 2:
                # Wall jump mechanic
                self.velocity_y = self.jump_power * 0.8
                self.velocity_x = -self.velocity_x * 0.6
                self.wall_jump_available = False

        # Combat system
        if keys[self.controls['attack']] and self.attack_cooldown <= 0:
            self.attack()

        # Dash mechanic
        if keys[self.controls.get('dash', pygame.K_LSHIFT)] and self.dash_cooldown <= 0:
            self.dash()

    def dash(self):
        if self.dash_cooldown <= 0:
            dash_direction = 1 if self.facing_right else -1
            self.velocity_x += self.dash_power * dash_direction
            self.dash_cooldown = 60  # 1 second cooldown
            self.animation_state = "dashing"

    def attack(self):
        if self.attack_cooldown <= 0:
            self.is_attacking = True
            self.attack_cooldown = self.attack_cooldown_max
            self.animation_state = "attacking"
            self.animation_frame = 0

            # Add screen shake for impact
            self.screen_shake = 10

    def update(self, ground_y, screen_width):
        # Update all timers
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.hit_cooldown > 0:
            self.hit_cooldown -= 1
        if self.stun_timer > 0:
            self.stun_timer -= 1
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1
        if self.screen_shake > 0:
            self.screen_shake -= 1

        # Update power-up effects
        expired_powers = []
        for power_type, duration in list(self.power_duration.items()):
            self.power_duration[power_type] = duration - 1
            if duration <= 1:
                expired_powers.append(power_type)

        for power_type in expired_powers:
            if power_type in self.power_effects:
                del self.power_effects[power_type]
            if power_type in self.power_duration:
                del self.power_duration[power_type]

        # Apply power-up effects
        speed_multiplier = self.power_effects.get('speed', 1.0)
        damage_multiplier = self.power_effects.get('damage', 1.0)

        # Ultra-realistic physics
        self.velocity_x += self.knockback_x
        self.velocity_y += self.knockback_y
        self.knockback_x *= 0.7
        self.knockback_y *= 0.7

        # Apply friction and air resistance
        if self.on_ground:
            self.velocity_x *= self.friction
        else:
            self.velocity_x *= self.air_resistance

        # Speed limits with power-up consideration
        max_speed = self.max_speed * speed_multiplier
        if abs(self.velocity_x) > max_speed:
            self.velocity_x = max_speed if self.velocity_x > 0 else -max_speed

        # Gravity application
        if not self.on_ground:
            self.velocity_y += self.gravity
            # Terminal velocity
            if self.velocity_y > 20:
                self.velocity_y = 20

        # Update position with realistic movement
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Movement trail for visual effects
        self.movement_trail.append((self.x + self.width//2, self.y + self.height//2))
        if len(self.movement_trail) > 5:
            self.movement_trail.pop(0)

        # Screen boundaries with realistic collision
        if self.x < 0:
            self.x = 0
            self.velocity_x = abs(self.velocity_x) * 0.3  # Bounce effect
        elif self.x + self.width > screen_width:
            self.x = screen_width - self.width
            self.velocity_x = -abs(self.velocity_x) * 0.3

        # Ground collision with realistic physics
        if self.y + self.height >= ground_y:
            self.y = ground_y - self.height
            if self.velocity_y > 0:
                self.velocity_y = -self.velocity_y * 0.1  # Small bounce
            else:
                self.velocity_y = 0
            self.on_ground = True
            if self.animation_state == "jumping":
                self.animation_state = "idle"
        else:
            self.on_ground = False

        # Update animations
        self.update_animation()
        self.update_particles()
        self.update_damage_numbers()

        # Reset attack state
        if self.is_attacking and self.animation_frame >= 4:
            self.is_attacking = False

        # Combo system
        current_time = time.time()
        if current_time - self.last_hit_time > 2.0:
            self.combo_count = 0

    def update_animation(self):
        self.animation_timer += 1

        frame_speed = 6 if 'speed' in self.power_effects else 8

        if self.animation_timer >= frame_speed:
            self.animation_timer = 0
            self.animation_frame += 1

            if self.animation_state == "idle":
                if self.animation_frame >= 4:
                    self.animation_frame = 0
            elif self.animation_state == "running":
                if self.animation_frame >= 8:
                    self.animation_frame = 0
            elif self.animation_state == "attacking":
                if self.animation_frame >= 5:
                    self.animation_frame = 0
                    self.animation_state = "idle"
            elif self.animation_state == "jumping":
                if self.animation_frame >= 3:
                    self.animation_frame = 2
            elif self.animation_state == "dashing":
                if self.animation_frame >= 3:
                    self.animation_frame = 0
                    self.animation_state = "idle"

    def update_particles(self):
        # Update power-up particles
        self.power_particles = [(x, y, life-1, color) for x, y, life, color in self.power_particles if life > 0]

        # Add new particles for active power-ups
        if self.power_effects and random.random() < 0.3:
            colors = {
                'speed': (255, 255, 0),
                'damage': (255, 0, 0),
                'shield': (0, 0, 255),
                'rage': (255, 0, 255)
            }
            for power_type in self.power_effects:
                if power_type in colors:
                    self.power_particles.append((
                        self.x + random.randint(-10, 10),
                        self.y + random.randint(-10, 10),
                        30,
                        colors[power_type]
                    ))

    def update_damage_numbers(self):
        # Update floating damage numbers
        self.damage_numbers = [(x, y-1, life-1, damage, color) 
                              for x, y, life, damage, color in self.damage_numbers if life > 0]

    def take_damage(self, damage, attacker_x):
        if self.hit_cooldown <= 0:
            # Apply power-up damage reduction
            damage_reduction = self.power_effects.get('shield', 0)
            actual_damage = int(damage * (1.0 - damage_reduction))

            self.health -= actual_damage
            self.hit_cooldown = 30
            self.stun_timer = 15
            self.last_hit_time = time.time()

            # Add damage number
            self.damage_numbers.append((
                self.x + self.width//2,
                self.y - 10,
                60,
                actual_damage,
                (255, 100, 100)
            ))

            # Realistic knockback system
            knockback_force = 10 + (actual_damage * 0.3)
            if attacker_x < self.x:
                self.knockback_x = knockback_force
            else:
                self.knockback_x = -knockback_force
            self.knockback_y = -6

            # Screen shake
            self.screen_shake = 15

            return actual_damage
        return 0

    def apply_power_up(self, power_type):
        duration = 300  # 5 seconds at 60 FPS

        power_configs = {
            "speed": {'effect': 2.0, 'duration': duration},
            "damage": {'effect': 2.5, 'duration': duration},
            "shield": {'effect': 0.6, 'duration': duration},  # 60% damage reduction
            "heal": {'effect': 40, 'duration': 0},
            "rage": {'effects': {'speed': 1.7, 'damage': 2.2}, 'duration': duration},
            "invincible": {'effect': 1.0, 'duration': 120},  # 2 seconds
            "freeze": {'effect': 1.0, 'duration': 90}  # 1.5 seconds
        }

        if power_type in power_configs:
            config = power_configs[power_type]

            if power_type == "heal":
                self.health = min(self.max_health, self.health + config['effect'])
            elif power_type == "rage":
                for effect, value in config['effects'].items():
                    self.power_effects[effect] = value
                    self.power_duration[effect] = config['duration']
            else:
                self.power_effects[power_type] = config['effect']
                if config['duration'] > 0:
                    self.power_duration[power_type] = config['duration']

    def get_attack_rect(self):
        if not self.is_attacking:
            return None

        range_multiplier = self.power_effects.get('damage', 1.0)
        attack_range = int(self.attack_range * range_multiplier)

        if self.facing_right:
            attack_x = self.x + self.width
        else:
            attack_x = self.x - attack_range

        return pygame.Rect(attack_x, self.y, attack_range, self.height)

    def draw(self, screen):
        # Screen shake effect
        shake_x = random.randint(-self.screen_shake, self.screen_shake) if self.screen_shake > 0 else 0
        shake_y = random.randint(-self.screen_shake, self.screen_shake) if self.screen_shake > 0 else 0

        # Draw movement trail
        for i, (trail_x, trail_y) in enumerate(self.movement_trail[:-1]):
            alpha = int(50 * (i / len(self.movement_trail)))
            trail_color = [c + alpha for c in self.color]
            trail_color = [min(255, c) for c in trail_color]
            pygame.draw.circle(screen, trail_color, 
                             (int(trail_x + shake_x), int(trail_y + shake_y)), 3)

        # Pixelated character rendering
        pixel_size = 4

        # Dynamic color based on power-ups and state
        body_color = list(self.color)

        # Power-up visual effects
        if 'speed' in self.power_effects:
            body_color[1] = min(255, body_color[1] + 70)  # Yellow tint
        if 'shield' in self.power_effects:
            body_color[2] = min(255, body_color[2] + 70)  # Blue tint
        if 'damage' in self.power_effects:
            body_color[0] = min(255, body_color[0] + 70)  # Red tint
        if 'invincible' in self.power_effects:
            # Rainbow effect
            time_factor = time.time() * 10
            body_color = [
                int(127 + 127 * math.sin(time_factor)),
                int(127 + 127 * math.sin(time_factor + 2)),
                int(127 + 127 * math.sin(time_factor + 4))
            ]

        # Hit flash effect
        if self.hit_cooldown > 0 and self.hit_cooldown % 6 < 3:
            body_color = [255, 255, 255]

        # Ultra-detailed pixelated character
        for y in range(0, self.height, pixel_size):
            for x in range(0, self.width, pixel_size):
                rel_x = x / self.width
                rel_y = y / self.height

                should_draw = False
                pixel_color = body_color[:]

                # Complex humanoid shape with animation
                if self.animation_state == "idle":
                    # Standing pose with breathing animation
                    breathing = int(2 * math.sin(self.animation_frame * 0.3))
                    if (0.25 < rel_x < 0.75 and 0.15 < rel_y < 0.85) or                        (0.35 < rel_x < 0.65 and 0.0 < rel_y < 1.0):
                        should_draw = True

                elif self.animation_state == "running":
                    # Running animation with leg movement
                    leg_offset = int(4 * math.sin(self.animation_frame))
                    if (0.25 < rel_x < 0.75 and 0.15 < rel_y < 0.7) or                        (0.35 < rel_x < 0.65 and 0.0 < rel_y < 0.85):
                        should_draw = True

                elif self.animation_state == "attacking":
                    # Extended attack pose
                    if self.facing_right:
                        attack_extend = min(self.animation_frame * 0.1, 0.3)
                        if (0.2 < rel_x < 0.8 + attack_extend and 0.1 < rel_y < 0.9):
                            should_draw = True
                            pixel_color[0] = min(255, pixel_color[0] + 50)  # Red tint for attack
                    else:
                        attack_extend = min(self.animation_frame * 0.1, 0.3)
                        if (0.2 - attack_extend < rel_x < 0.8 and 0.1 < rel_y < 0.9):
                            should_draw = True
                            pixel_color[0] = min(255, pixel_color[0] + 50)

                elif self.animation_state == "jumping":
                    # Compact jumping pose
                    if (0.3 < rel_x < 0.7 and 0.2 < rel_y < 0.8):
                        should_draw = True

                elif self.animation_state == "dashing":
                    # Stretched dashing pose
                    if (0.1 < rel_x < 0.9 and 0.25 < rel_y < 0.75):
                        should_draw = True
                        pixel_color = [min(255, c + 100) for c in pixel_color]  # Bright dash effect

                if should_draw:
                    # Animation offsets
                    offset_x = 0
                    offset_y = 0

                    if self.animation_state == "running":
                        offset_x = int(2 * math.sin(self.animation_frame * 0.8))
                        offset_y = int(1 * math.sin(self.animation_frame * 1.6))
                    elif self.animation_state == "attacking":
                        if self.facing_right:
                            offset_x = self.animation_frame * 3
                        else:
                            offset_x = -self.animation_frame * 3

                    # Add random pixel noise for texture
                    if random.random() < 0.1:
                        pixel_color = [max(0, c - 20) for c in pixel_color]

                    pixel_rect = pygame.Rect(
                        int(self.x + x + offset_x + shake_x),
                        int(self.y + y + offset_y + shake_y),
                        pixel_size,
                        pixel_size
                    )
                    pygame.draw.rect(screen, pixel_color, pixel_rect)

        # Draw power-up particles
        for px, py, life, color in self.power_particles:
            alpha = int(255 * (life / 30))
            particle_color = [min(255, c + alpha//4) for c in color]
            pygame.draw.circle(screen, particle_color, 
                             (int(px + shake_x), int(py + shake_y)), 2)

        # Draw attack indicators
        if self.is_attacking:
            attack_rect = self.get_attack_rect()
            if attack_rect:
                # Dynamic attack visualization
                attack_intensity = int(255 * (self.animation_frame / 4))
                attack_color = (255, attack_intensity, attack_intensity)
                pygame.draw.rect(screen, attack_color, 
                               (attack_rect.x + shake_x, attack_rect.y + shake_y, 
                                attack_rect.width, attack_rect.height), 3)

                # Attack particles
                for _ in range(5):
                    px = attack_rect.x + random.randint(0, attack_rect.width)
                    py = attack_rect.y + random.randint(0, attack_rect.height)
                    pygame.draw.circle(screen, (255, 255, 0), 
                                     (int(px + shake_x), int(py + shake_y)), 2)

        # Draw damage numbers
        for dx, dy, life, damage, color in self.damage_numbers:
            alpha = int(255 * (life / 60))
            damage_color = [min(255, c * (alpha / 255)) for c in color]
            # Note: In a real implementation, you'd need font rendering here
            pygame.draw.circle(screen, damage_color, 
                             (int(dx + shake_x), int(dy + shake_y)), 3)

    def draw_health_bar(self, screen, x, y):
     bar_width = 250
     bar_height = 25

     for i in range(bar_height):
        gradient_color = (30 + i * 2, 30 + i * 2, 30 + i * 2)
        pygame.draw.rect(screen, gradient_color, (x, y + i, bar_width, 1))

     health_ratio = self.health / self.max_health
     health_width = int(health_ratio * bar_width)
     if health_ratio > 0.6:
        health_color = (0, int(255 * health_ratio), 0)
     elif health_ratio > 0.3:
        health_color = (255, 255, 0)
     else:
        health_color = (255, int(255 * health_ratio), 0)
        
     if health_ratio < 0.25:
        pulse = int(50 * math.sin(time.time() * 10))
        # Use clamp and int for each component to keep it within 0-255
        health_color = tuple(max(0, min(255, int(c + pulse))) for c in health_color)

    # Ensure all color components are ints and within 0-255
     health_color = tuple(max(0, min(255, int(c))) for c in health_color)
     pygame.draw.rect(screen, health_color, (x, y, health_width, bar_height))

    # ... rest of method unchanged ...


        # Power-up indicators on health bar
     if self.power_effects:
            indicator_width = bar_width // len(self.power_effects)
            for i, power_type in enumerate(self.power_effects):
                power_colors = {
                    'speed': (255, 255, 0),
                    'damage': (255, 0, 0),
                    'shield': (0, 0, 255),
                    'rage': (255, 0, 255),
                    'invincible': (255, 255, 255)
                }
                if power_type in power_colors:
                    pygame.draw.rect(screen, power_colors[power_type], 
                                   (x + i * indicator_width, y - 5, indicator_width - 2, 3))

        # Border with dynamic effect
     border_color = (255, 255, 255) if not self.power_effects else (255, 255, 0)
     pygame.draw.rect(screen, border_color, (x, y, bar_width, bar_height), 3)

class PowerUp:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 35
        self.height = 35

        # Expanded power-up types
        power_types = ["speed", "damage", "shield", "heal", "rage", "invincible", "freeze"]
        weights = [20, 20, 15, 25, 10, 5, 5]  # Weighted random selection
        self.type = random.choices(power_types, weights=weights)[0]

        self.collected = False
        self.spawn_time = time.time()
        self.pulse_timer = 0
        self.float_offset = 0
        self.rotation = 0
        self.particles = []

        # Enhanced color coding
        self.colors = {
            "speed": (255, 255, 0),      # Yellow
            "damage": (255, 50, 50),     # Red
            "shield": (50, 50, 255),     # Blue
            "heal": (50, 255, 50),       # Green
            "rage": (255, 50, 255),      # Magenta
            "invincible": (255, 255, 255), # White
            "freeze": (150, 255, 255)    # Cyan
        }

        self.descriptions = {
            "speed": "SPEED BOOST",
            "damage": "DAMAGE UP",
            "shield": "DAMAGE SHIELD",
            "heal": "HEALTH RESTORE",
            "rage": "BERSERKER MODE",
            "invincible": "INVINCIBILITY",
            "freeze": "TIME FREEZE"
        }

    def update(self):
        self.pulse_timer += 1
        self.float_offset = math.sin(self.pulse_timer * 0.1) * 5
        self.rotation += 2

        # Generate particles
        if random.random() < 0.3:
            self.particles.append({
                'x': self.x + self.width//2 + random.randint(-10, 10),
                'y': self.y + self.height//2 + random.randint(-10, 10),
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(-3, -1),
                'life': 30,
                'color': self.colors[self.type]
            })

        # Update particles
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.1  # Gravity
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.particles.remove(particle)

        # Remove after 15 seconds
        if time.time() - self.spawn_time > 15:
            return False
        return True

    def check_collision(self, fighter):
        fighter_rect = pygame.Rect(fighter.x, fighter.y, fighter.width, fighter.height)
        power_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        if fighter_rect.colliderect(power_rect) and not self.collected:
            fighter.apply_power_up(self.type)
            self.collected = True

            # Spawn collection effect particles
            for _ in range(15):
                fighter.power_particles.append((
                    self.x + self.width//2,
                    self.y + self.height//2,
                    60,
                    self.colors[self.type]
                ))

            return True
        return False

    def draw(self, screen):
        if self.collected:
            return

        color = self.colors[self.type]

        # Enhanced pulsing effect
        pulse = int(30 * math.sin(self.pulse_timer * 0.15))
        size = self.width + pulse // 6

        # Floating animation
        draw_y = self.y + self.float_offset

        # Draw particles first
        for particle in self.particles:
            alpha = int(255 * (particle['life'] / 30))
            particle_color = [min(255, c + alpha//3) for c in particle['color']]
            pygame.draw.circle(screen, particle_color, 
                             (int(particle['x']), int(particle['y'])), 2)

        # Enhanced pixelated power-up with rotation effect
        pixel_size = 3
        center_x, center_y = self.x + self.width//2, draw_y + self.height//2

        for y in range(0, size, pixel_size):
            for x in range(0, size, pixel_size):
                # Apply rotation
                rel_x = (x - size//2) / size * 2
                rel_y = (y - size//2) / size * 2

                # Rotate coordinates
                angle = math.radians(self.rotation)
                rot_x = rel_x * math.cos(angle) - rel_y * math.sin(angle)
                rot_y = rel_x * math.sin(angle) + rel_y * math.cos(angle)

                # Complex power-up shapes
                should_draw = False

                if self.type == "speed":
                    # Lightning bolt shape
                    if abs(rot_x) < 0.6 and abs(rot_y) < 0.8:
                        should_draw = True
                elif self.type == "damage":
                    # Sword/blade shape
                    if (abs(rot_x) < 0.3 and abs(rot_y) < 0.9) or (abs(rot_x) < 0.8 and abs(rot_y) < 0.3):
                        should_draw = True
                elif self.type == "shield":
                    # Shield shape
                    if rot_x*rot_x + rot_y*rot_y < 0.7:
                        should_draw = True
                elif self.type == "heal":
                    # Cross shape
                    if (abs(rot_x) < 0.3 and abs(rot_y) < 0.9) or (abs(rot_x) < 0.9 and abs(rot_y) < 0.3):
                        should_draw = True
                else:
                    # Star shape for special powers
                    if (abs(rot_x) < 0.6 and abs(rot_y) < 0.6) and                        (abs(rot_x) < 0.3 or abs(rot_y) < 0.3 or abs(rot_x + rot_y) < 0.6 or abs(rot_x - rot_y) < 0.6):
                        should_draw = True

                if should_draw:
                    # Enhanced color with effects
                    bright_color = [max(0,min(255, int(c + pulse + random.randint(-20, 20))
                                              )) for c in color]

                    # Special effects for rare power-ups
                    if self.type == "invincible":
                        # Rainbow effect
                        time_factor = time.time() * 5 + (rot_x + rot_y) * 10
                        bright_color = [
                            int(127 + 127 * math.sin(time_factor)),
                            int(127 + 127 * math.sin(time_factor + 2)),
                            int(127 + 127 * math.sin(time_factor + 4))
                        ]

                    pixel_rect = pygame.Rect(
                        int(center_x + rot_x * size//2 - pixel_size//2),
                        int(center_y + rot_y * size//2 - pixel_size//2),
                        pixel_size,
                        pixel_size
                    )
                    pygame.draw.rect(screen, bright_color, pixel_rect)

        # Glowing outline effect
        outline_color = [min(255, c + 100) for c in color]
        pygame.draw.circle(screen, outline_color, 
                         (int(center_x), int(center_y)), size//2 + 5, 2)

class Game:
    def __init__(self):
        pygame.init()

        self.screen_width = 1200
        self.screen_height = 700
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Ultra-Realistic Street Fight - Pixelated Combat")

        self.clock = pygame.time.Clock()
        self.ground_y = self.screen_height - 120

        # Player controls
        player1_controls = {
            'left': pygame.K_a,
            'right': pygame.K_d,
            'jump': pygame.K_w,
            'attack': pygame.K_SPACE,
            'dash': pygame.K_LSHIFT
        }

        player2_controls = {
            'left': pygame.K_LEFT,
            'right': pygame.K_RIGHT,
            'jump': pygame.K_UP,
            'attack': pygame.K_RETURN,
            'dash': pygame.K_RSHIFT
        }

        # Create fighters with distinct colors
        self.fighter1 = Fighter(150, self.ground_y - 60, player1_controls, (255, 100, 100))
        self.fighter2 = Fighter(self.screen_width - 200, self.ground_y - 60, player2_controls, (100, 100, 255))

        # Game state
        self.power_ups = []
        self.power_spawn_timer = 0
        self.power_spawn_interval = 240  # 4 seconds at 60 FPS
        self.game_over = False
        self.winner = None
        self.round_number = 1
        self.p1_wins = 0
        self.p2_wins = 0

        # Visual effects
        self.background_particles = []
        self.screen_shake = 0

        # Initialize fonts
        try:
            self.big_font = pygame.font.Font(None, 48)
            self.font = pygame.font.Font(None, 36)
            self.small_font = pygame.font.Font(None, 24)
        except:
            self.big_font = None
            self.font = None
            self.small_font = None

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.game_over:
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        running = False

            if not self.game_over:
                self.update()

            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    def update(self):
        keys = pygame.key.get_pressed()

        # Update fighters
        self.fighter1.handle_input(keys)
        self.fighter2.handle_input(keys)

        self.fighter1.update(self.ground_y, self.screen_width)
        self.fighter2.update(self.ground_y, self.screen_width)

        # Combat system
        self.check_combat()

        # Power-up spawning system
        self.power_spawn_timer += 1
        if self.power_spawn_timer >= self.power_spawn_interval:
            self.spawn_power_up()
            self.power_spawn_timer = 0
            # Decrease spawn interval slightly each round for faster gameplay
            self.power_spawn_interval = max(120, self.power_spawn_interval - 5)

        # Update power-ups
        self.power_ups = [p for p in self.power_ups if p.update()]

        # Check power-up collisions
        for power_up in self.power_ups[:]:
            if power_up.check_collision(self.fighter1) or power_up.check_collision(self.fighter2):
                self.power_ups.remove(power_up)

        # Update background effects
        self.update_background_effects()

        # Check for round end
        if self.fighter1.health <= 0:
            self.end_round("Player 2")
        elif self.fighter2.health <= 0:
            self.end_round("Player 1")

    def check_combat(self):
        damage_dealt = False

        # Fighter 1 attacking Fighter 2
        if self.fighter1.is_attacking:
            attack_rect = self.fighter1.get_attack_rect()
            if attack_rect:
                fighter2_rect = pygame.Rect(self.fighter2.x, self.fighter2.y, 
                                          self.fighter2.width, self.fighter2.height)
                if attack_rect.colliderect(fighter2_rect):
                    base_damage = self.fighter1.attack_damage
                    damage_multiplier = self.fighter1.power_effects.get('damage', 1.0)
                    final_damage = int(base_damage * damage_multiplier)

                    actual_damage = self.fighter2.take_damage(final_damage, self.fighter1.x)
                    if actual_damage > 0:
                        self.fighter1.combo_count += 1
                        damage_dealt = True

        # Fighter 2 attacking Fighter 1
        if self.fighter2.is_attacking:
            attack_rect = self.fighter2.get_attack_rect()
            if attack_rect:
                fighter1_rect = pygame.Rect(self.fighter1.x, self.fighter1.y, 
                                          self.fighter1.width, self.fighter1.height)
                if attack_rect.colliderect(fighter1_rect):
                    base_damage = self.fighter2.attack_damage
                    damage_multiplier = self.fighter2.power_effects.get('damage', 1.0)
                    final_damage = int(base_damage * damage_multiplier)

                    actual_damage = self.fighter1.take_damage(final_damage, self.fighter2.x)
                    if actual_damage > 0:
                        self.fighter2.combo_count += 1
                        damage_dealt = True

        # Add screen shake for successful hits
        if damage_dealt:
            self.screen_shake = 8

    def spawn_power_up(self):
        # Strategic power-up placement
        available_positions = [
            (200, self.ground_y - 50),
            (self.screen_width - 250, self.ground_y - 50),
            (self.screen_width // 2, self.ground_y - 50),
            (300, self.ground_y - 50),
            (self.screen_width - 350, self.ground_y - 50)
        ]

        # Avoid spawning too close to fighters
        valid_positions = []
        for pos in available_positions:
            if abs(pos[0] - self.fighter1.x) > 100 and abs(pos[0] - self.fighter2.x) > 100:
                valid_positions.append(pos)

        if valid_positions:
            x, y = random.choice(valid_positions)
            power_up = PowerUp(x, y)
            self.power_ups.append(power_up)

    def update_background_effects(self):
        # Update screen shake
        if self.screen_shake > 0:
            self.screen_shake -= 1

        # Generate background particles
        if random.random() < 0.1:
            self.background_particles.append({
                'x': random.randint(0, self.screen_width),
                'y': self.screen_height,
                'vx': random.uniform(-1, 1),
                'vy': random.uniform(-3, -1),
                'life': random.randint(60, 120),
                'color': (100, 100, 150),
                'size': random.randint(1, 3)
            })

        # Update background particles
        for particle in self.background_particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            if particle['life'] <= 0 or particle['y'] < 0:
                self.background_particles.remove(particle)

    def end_round(self, winner):
        
        if winner == "Player 1":
            self.p1_wins += 1
        else:
            self.p2_wins += 1

        # Best of 3 rounds
        if self.p1_wins >= 9 or self.p2_wins >= 9:
            self.game_over = True
            self.winner = winner
        else:
            # Reset for next round
            self.round_number += 1
            self.reset_round()

    def reset_round(self):
        # Reset fighter positions and health
        self.fighter1.x = 150
        self.fighter2.x = self.screen_width - 200
        self.fighter1.y = self.ground_y - 60
        self.fighter2.y = self.ground_y - 60
        self.fighter1.health = self.fighter1.max_health
        self.fighter2.health = self.fighter2.max_health

        # Reset velocities and states
        for fighter in [self.fighter1, self.fighter2]:
            fighter.velocity_x = 0
            fighter.velocity_y = 0
            fighter.power_effects.clear()
            fighter.power_duration.clear()
            fighter.animation_state = "idle"
            fighter.is_attacking = False
            fighter.hit_cooldown = 0
            fighter.stun_timer = 0
            fighter.combo_count = 0

        # Clear power-ups
        self.power_ups.clear()
        self.power_spawn_timer = 0

    def draw(self):
        # Screen shake effect
        shake_x = random.randint(-self.screen_shake, self.screen_shake) if self.screen_shake > 0 else 0
        shake_y = random.randint(-self.screen_shake, self.screen_shake) if self.screen_shake > 0 else 0

        # Dynamic background
        bg_color = (30, 30, 60)
        if self.screen_shake > 5:
            bg_color = tuple(min(255, c + self.screen_shake * 5) for c in bg_color)

        self.screen.fill(bg_color)

        # Draw background particles
        for particle in self.background_particles:
            alpha = int(255 * (particle['life'] / 120))
            color = [min(255, c + alpha//4) for c in particle['color']]
            pygame.draw.circle(self.screen, color, 
                             (int(particle['x'] + shake_x), int(particle['y'] + shake_y)), 
                             particle['size'])

        # Ground with texture
        ground_color = (80, 60, 40)
        pygame.draw.rect(self.screen, ground_color, 
                        (0, self.ground_y, self.screen_width, self.screen_height - self.ground_y))

        # Ground details
        for i in range(0, self.screen_width, 20):
            detail_color = (ground_color[0] + random.randint(-10, 10),
                           ground_color[1] + random.randint(-10, 10),
                           ground_color[2] + random.randint(-10, 10))
            detail_color = tuple(max(0, min(255, c)) for c in detail_color)
            pygame.draw.rect(self.screen, detail_color, 
                           (i + shake_x, self.ground_y + shake_y, 18, 
                            self.screen_height - self.ground_y))

        # Draw fighters
        self.fighter1.draw(self.screen)
        self.fighter2.draw(self.screen)

        # Draw power-ups
        for power_up in self.power_ups:
            power_up.draw(self.screen)

        # UI Elements
        self.draw_ui()

        # Game over screen
        if self.game_over:
            self.draw_game_over_screen()

        pygame.display.flip()

    def draw_ui(self):
        # Health bars
        self.fighter1.draw_health_bar(self.screen, 50, 30)
        self.fighter2.draw_health_bar(self.screen, self.screen_width - 300, 30)

        if self.font:
            # Player names
            p1_text = self.font.render("PLAYER 1", True, (255, 255, 255))
            p2_text = self.font.render("PLAYER 2", True, (255, 255, 255))
            self.screen.blit(p1_text, (50, 5))
            self.screen.blit(p2_text, (self.screen_width - 300, 5))

            # Round counter
            round_text = self.big_font.render(f"ROUND {self.round_number}", True, (255, 255, 0))
            round_rect = round_text.get_rect(center=(self.screen_width // 2, 40))
            self.screen.blit(round_text, round_rect)

            # Win counter
            wins_text = self.font.render(f"{self.p1_wins} - {self.p2_wins}", True, (255, 255, 255))
            wins_rect = wins_text.get_rect(center=(self.screen_width // 2, 70))
            self.screen.blit(wins_text, wins_rect)

        if self.small_font:
            # Controls
            controls_text = self.small_font.render(
                "P1: WASD + SPACE + SHIFT | P2: ARROWS + ENTER + RIGHT SHIFT", 
                True, (200, 200, 200)
            )
            self.screen.blit(controls_text, (20, self.screen_height - 25))

            # Power-up info
            if self.power_ups:
                power_text = self.small_font.render(
                    f"Active Power-ups: {len(self.power_ups)}", 
                    True, (255, 255, 0)
                )
                self.screen.blit(power_text, (self.screen_width - 200, self.screen_height - 25))

    def draw_game_over_screen(self):
        if not self.font:
            return

        # Semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Winner announcement
        winner_text = self.big_font.render(f"{self.winner} WINS THE MATCH!", True, (255, 255, 0))
        winner_rect = winner_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
        self.screen.blit(winner_text, winner_rect)

        # Final score
        score_text = self.font.render(f"Final Score: {self.p1_wins} - {self.p2_wins}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        self.screen.blit(score_text, score_rect)

        # Instructions
        restart_text = self.font.render("Press R to restart or ESC to quit", True, (200, 200, 200))
        restart_rect = restart_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50))
        self.screen.blit(restart_text, restart_rect)

    def reset_game(self):
        # Full game reset
        self.round_number = 1
        self.p1_wins = 0
        self.p2_wins = 0
        self.game_over = False
        self.winner = None
        self.power_spawn_interval = 240

        self.reset_round()

if __name__ == "__main__":
    game = Game()
    game.run()
