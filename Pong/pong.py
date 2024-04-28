import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BALL_SPEED = 2
PADDLE_SPEED = 2
WINNING_SCORE = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# Initialize ball and paddles
ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
player_red_paddle = pygame.Rect(50, HEIGHT // 2 - 60, 10, 120)
player_green_paddle = pygame.Rect(WIDTH - 60, HEIGHT // 2 - 60, 10, 120)

# Ball movement variables
ball_speed_x = BALL_SPEED
ball_speed_y = BALL_SPEED

# Paddle movement variables
player_red_paddle_speed = 0
player_green_paddle_speed = 0

# Scores
player_red_score = 0
player_green_score = 0

# Fonts
font = pygame.font.Font(None, 36)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_green_paddle_speed = -PADDLE_SPEED
            if event.key == pygame.K_DOWN:
                player_green_paddle_speed = PADDLE_SPEED
            if event.key == pygame.K_w:
                player_red_paddle_speed = -PADDLE_SPEED
            if event.key == pygame.K_s:
                player_red_paddle_speed = PADDLE_SPEED

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player_green_paddle_speed = 0
            if event.key == pygame.K_w or event.key == pygame.K_s:
                player_red_paddle_speed = 0

    # Update paddles' positions
    player_red_paddle.y += player_red_paddle_speed
    player_green_paddle.y += player_green_paddle_speed

    # Ensure paddles don't go out of the screen
    player_red_paddle.y = max(0, min(HEIGHT - player_red_paddle.height, player_red_paddle.y))
    player_green_paddle.y = max(0, min(HEIGHT - player_green_paddle.height, player_green_paddle.y))

    # Update ball's position
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision with paddles
    if ball.colliderect(player_red_paddle) or ball.colliderect(player_green_paddle):
        ball_speed_x = -ball_speed_x

    # Ball collision with top and bottom walls
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y = -ball_speed_y

    # Player Red scores
    if ball.left <= 0:
        player_green_score += 1
        ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
        ball_speed_x = BALL_SPEED

    # Player Green scores
    if ball.right >= WIDTH:
        player_red_score += 1
        ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
        ball_speed_x = -BALL_SPEED

    # Check for a winner
    if player_red_score >= WINNING_SCORE:
        winner_message = font.render("Player Red wins!", True, WHITE)
        screen.blit(winner_message, (WIDTH // 2 - 120, HEIGHT // 2 - 18))
        pygame.display.flip()
        pygame.time.delay(2000)
        pygame.quit()
        sys.exit()
    elif player_green_score >= WINNING_SCORE:
        winner_message = font.render("Player Green wins!", True, WHITE)
        screen.blit(winner_message, (WIDTH // 2 - 120, HEIGHT // 2 - 18))
        pygame.display.flip()
        pygame.time.delay(2000)
        pygame.quit()
        sys.exit()

    # Clear the screen
    screen.fill(BLACK)

    # Draw paddles and ball
    pygame.draw.rect(screen, RED, player_red_paddle)
    pygame.draw.rect(screen, GREEN, player_green_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)

    # Draw score panels
    player_red_text = font.render(f"Player Red: {player_red_score}", True, WHITE)
    player_green_text = font.render(f"Player Green: {player_green_score}", True, WHITE)
    screen.blit(player_red_text, (20, 20))
    screen.blit(player_green_text, (WIDTH - 220, 20))

    # Update the display
    pygame.display.flip()

    # Control game speed (FPS)
    pygame.time.Clock().tick(60)
