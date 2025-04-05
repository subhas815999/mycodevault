import pygame
import sys

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
PADDLE_SPEED = 5
BALL_SPEED = 4

# Initialize
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong Game")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 50)


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


# Create game objects
paddle1 = Paddle(30)
paddle2 = Paddle(SCREEN_WIDTH - 40)
ball = Ball()

score1 = 0
score2 = 0

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Key press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                paddle1.speed = -PADDLE_SPEED
            if event.key == pygame.K_s:
                paddle1.speed = PADDLE_SPEED
            if event.key == pygame.K_UP:
                paddle2.speed = -PADDLE_SPEED
            if event.key == pygame.K_DOWN:
                paddle2.speed = PADDLE_SPEED

        # Key release
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_w, pygame.K_s):
                paddle1.speed = 0
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                paddle2.speed = 0

    # Move paddles and ball
    paddle1.move()
    paddle2.move()
    ball.move()

    # Paddle collision
    if ball.colliderect(paddle1) or ball.colliderect(paddle2):
        ball.dx *= -1

    # Scoring
    if ball.left <= 0:
        score2 += 1
        ball.reset()
    if ball.right >= SCREEN_WIDTH:
        score1 += 1
        ball.reset()

    # Draw everything
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, WHITE, paddle1)
    pygame.draw.rect(screen, WHITE, paddle2)
    pygame.draw.ellipse(screen, WHITE, ball)
    text = font.render(f"{score1} - {score2}", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - 50, 20))

    pygame.display.flip()
    clock.tick(60)
