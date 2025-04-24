import pygame
import sys
import random
import time

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
PADDLE_SPEED = 5
BALL_SPEED = 4

# Ask user for final point
try:
    final_point = int(input("Enter the final point to win the game: "))
except ValueError:
    print("Invalid input. Using default final point: 10")
    final_point = 10

# Initialize
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong Game")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 50)
large_font = pygame.font.Font(None, 100)


class Paddle(pygame.Rect):
    def __init__(self, x):
        super().__init__(x, SCREEN_HEIGHT // 2 - 50, 10, 100)
        self.speed = 0

    def move(self):
        self.y += self.speed
        self.y = max(0, min(self.y, SCREEN_HEIGHT - self.height))


class Ball(pygame.Rect):
    def __init__(self):
        super().__init__(SCREEN_WIDTH // 2 - 10, SCREEN_HEIGHT // 2 - 10, 20, 20)
        self.dx = BALL_SPEED
        self.dy = BALL_SPEED

    def move(self):
        self.x += self.dx
        self.y += self.dy
        if self.top <= 0 or self.bottom >= SCREEN_HEIGHT:
            self.dy *= -1

    def reset(self):
        self.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.dx *= -1


# Countdown before game starts
def countdown():
    for i in range(3, 0, -1):
        screen.fill((0, 0, 0))
        text = large_font.render(str(i), True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 50))
        pygame.display.flip()
        time.sleep(1)
    screen.fill((0, 0, 0))
    go_text = large_font.render("GO!", True, WHITE)
    screen.blit(go_text, (SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 - 50))
    pygame.display.flip()
    time.sleep(1)

# Game objects
paddle1 = Paddle(30)
paddle2 = Paddle(SCREEN_WIDTH - 40)
ball = Ball()
score1 = 0
score2 = 0
winner = None
bg_color = [0, 0, 0]
color_change = [random.choice([-1, 1]) for _ in range(3)]

# Run countdown
countdown()

# Game loop
running = True
while running:
    # Change background color
    for i in range(3):
        bg_color[i] += color_change[i] * 1
        if bg_color[i] >= 255 or bg_color[i] <= 0:
            color_change[i] *= -1
            bg_color[i] = max(0, min(255, bg_color[i]))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                paddle1.speed = -PADDLE_SPEED
            if event.key == pygame.K_s:
                paddle1.speed = PADDLE_SPEED
            if event.key == pygame.K_UP:
                paddle2.speed = -PADDLE_SPEED
            if event.key == pygame.K_DOWN:
                paddle2.speed = PADDLE_SPEED

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_w, pygame.K_s):
                paddle1.speed = 0
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                paddle2.speed = 0

    if winner is None:
        paddle1.move()
        paddle2.move()
        ball.move()

        if ball.colliderect(paddle1) or ball.colliderect(paddle2):
            ball.dx *= -1

        if ball.left <= 0:
            score2 += 1
            ball.reset()
        if ball.right >= SCREEN_WIDTH:
            score1 += 1
            ball.reset()

        # Check winner
        if score1 >= final_point:
            winner = "Player 1"
        elif score2 >= final_point:
            winner = "Player 2"

    # Draw
    screen.fill(tuple(bg_color))
    pygame.draw.rect(screen, WHITE, paddle1)
    pygame.draw.rect(screen, WHITE, paddle2)
    pygame.draw.ellipse(screen, WHITE, ball)
    text = font.render(f"{score1} - {score2}", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - 50, 20))

    if winner:
        win_text = font.render(f"{winner} Wins!", True, WHITE)
        screen.blit(win_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 25))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
