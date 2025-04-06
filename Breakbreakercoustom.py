import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

# Paddle dimensions
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
PADDLE_SPEED = 10

# Ball dimensions
BALL_RADIUS = 8

# Initialize clock
clock = pygame.time.Clock()


# Function to create bricks
def create_bricks(rows, cols, brick_width, brick_height):
    bricks = []
    for row in range(rows):
        for col in range(cols):
            brick_x = col * brick_width
            brick_y = row * brick_height
            brick = pygame.Rect(brick_x, brick_y, brick_width, brick_height)
            bricks.append(brick)
    return bricks


# Game loop function
def game_loop(level, brick_count):
    global PADDLE_WIDTH, ball_dx, ball_dy

    # Adjust difficulty settings based on level
    if level == "easy":
        PADDLE_WIDTH = 150
        ball_dx, ball_dy = 4, -4
    elif level == "medium":
        PADDLE_WIDTH = 100
        ball_dx, ball_dy = 6, -6
    elif level == "very hard":
        PADDLE_WIDTH = 80
        ball_dx, ball_dy = 8, -8

    # Determine rows, columns, and brick size based on the brick count and difficulty
    cols = 10 if level == "easy" else 15 if level == "medium" else 20
    rows = brick_count // cols
    brick_width = WIDTH // cols
    brick_height = HEIGHT // (rows * 5)
    bricks = create_bricks(rows, cols, brick_width, brick_height)

    # Paddle and ball
    paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 50, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)

    running = True

    while running:
        screen.fill(BLACK)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.move_ip(-PADDLE_SPEED, 0)
        if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
            paddle.move_ip(PADDLE_SPEED, 0)

        # Ball movement
        ball.x += ball_dx
        ball.y += ball_dy

        # Ball collision with walls
        if ball.left <= 0 or ball.right >= WIDTH:
            ball_dx = -ball_dx
        if ball.top <= 0:
            ball_dy = -ball_dy
        if ball.colliderect(paddle):
            ball_dy = -ball_dy

        # Ball collision with bricks
        for brick in bricks[:]:
            if ball.colliderect(brick):
                bricks.remove(brick)
                ball_dy = -ball_dy
                break

        # Ball falls below paddle
        if ball.bottom > HEIGHT:
            running = False  # End the game

        # Draw paddle, ball, and bricks
        pygame.draw.rect(screen, BLUE, paddle)
        pygame.draw.ellipse(screen, WHITE, ball)
        for brick in bricks:
            pygame.draw.rect(screen, RED, brick)

        # Check for win condition
        if not bricks:
            running = False  # End the game when all bricks are broken

        # Update screen
        pygame.display.flip()
        clock.tick(60)


# Brick quantity selection menu
def brick_menu(level):
    font = pygame.font.Font(None, 50)

    # Define buttons for brick quantities
    option1 = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 100, 200, 50)
    option2 = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50)
    option3 = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)

    while True:
        screen.fill(BLACK)

        # Draw title
        title_font = pygame.font.Font(None, 74)
        title_text = title_font.render("Select Brick Quantity", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

        # Draw buttons
        pygame.draw.rect(screen, GREEN, option1)
        pygame.draw.rect(screen, BLUE, option2)
        pygame.draw.rect(screen, RED, option3)

        if level == "easy":
            text1, text2, text3 = "20 Bricks", "40 Bricks", "60 Bricks"
        elif level == "medium":
            text1, text2, text3 = "50 Bricks", "100 Bricks", "150 Bricks"
        elif level == "very hard":
            text1, text2, text3 = "100 Bricks", "200 Bricks", "300 Bricks"

        screen.blit(font.render(text1, True, BLACK), (option1.x + 30, option1.y + 10))
        screen.blit(font.render(text2, True, BLACK), (option2.x + 30, option2.y + 10))
        screen.blit(font.render(text3, True, BLACK), (option3.x + 30, option3.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Check which option is clicked
                if option1.collidepoint(mouse_pos):
                    game_loop(level, int(text1.split()[0]))
                elif option2.collidepoint(mouse_pos):
                    game_loop(level, int(text2.split()[0]))
                elif option3.collidepoint(mouse_pos):
                    game_loop(level, int(text3.split()[0]))


# Main menu
def main_menu():
    font = pygame.font.Font(None, 50)

    # Define buttons
    easy_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 100, 200, 50)
    medium_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50)
    hard_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)

    while True:
        screen.fill(BLACK)

        # Draw title
        title_font = pygame.font.Font(None, 74)
        title_text = title_font.render("Brick Breaker", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

        # Draw buttons
        pygame.draw.rect(screen, GREEN, easy_button)
        pygame.draw.rect(screen, BLUE, medium_button)
        pygame.draw.rect(screen, RED, hard_button)

        easy_text = font.render("Easy", True, BLACK)
        medium_text = font.render("Medium", True, BLACK)
        hard_text = font.render("Very Hard", True, BLACK)

        screen.blit(easy_text, (easy_button.x + 50, easy_button.y + 10))
        screen.blit(medium_text, (medium_button.x + 30, medium_button.y + 10))
        screen.blit(hard_text, (hard_button.x + 20, hard_button.y + 10))

        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Check which button is clicked
                if easy_button.collidepoint(mouse_pos):
                    brick_menu("easy")
                elif medium_button.collidepoint(mouse_pos):
                    brick_menu("medium")
                elif hard_button.collidepoint(mouse_pos):
                    brick_menu("very hard")


# Run the game
main_menu()
