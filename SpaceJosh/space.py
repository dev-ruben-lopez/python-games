#from tkinter import font
#import fontTools
import pygame
import sys
import random
import time
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 700
CANNON_SPEED = 5
BULLET_SPEED = 8
ENEMY_SPEED = 1


# variables
player_name = "JOSHUA"
player_score = 0

#player_name = input("Enter Player Name: ")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders by Ruben - 2023")
background_image = pygame.image.load("img/background_city_01.png")
background_image = pygame.transform.scale(background_image,(800, 600))


#initialize top bar with data
top_bar = pygame.Rect(0,0,SCREEN_WIDTH,50)

# Initialize cannon
#cannon = pygame.Rect(WIDTH // 2 - 30, HEIGHT - 50, 60, 20)
cannon = pygame.Rect(SCREEN_WIDTH // 2 - 15, SCREEN_HEIGHT - 20, 20, 10)
cannon_barrel = pygame.Rect(SCREEN_WIDTH // 2 - 8, SCREEN_HEIGHT - 50, 5, 20)

# Initialize sound effects
pygame.mixer.init()
shoot_sound = pygame.mixer.Sound("sounds/shoot1.flac")  
win_sound = pygame.mixer.Sound("sounds/win.wav")  
lose_sound = pygame.mixer.Sound("sounds/game_over.wav")  

# Initialize game state
game_over = False
new_game = False
enemies_number = 3
# Initialize bullets
bullets = []

# Initialize enemies
#enemies = [pygame.Rect(random.randint(10, SCREEN_WIDTH - 10), random.randint(50, 200), 20, 20) for _ in range(enemies_number)]

enemy_images = [
    pygame.image.load("img/alien01.png"),  # Replace "enemy1.png" with the image of the first enemy
    pygame.image.load("img/alien02.png"),  # Replace "enemy2.png" with the image of the second enemy
    pygame.image.load("img/alien03.png"),  # Replace "enemy3.png" with the image of the third enemy
]

enemy_image_for_round = 0;

enemies = [
    pygame.Rect(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, 200), 40, 40),
    pygame.Rect(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, 200), 40, 40),
    pygame.Rect(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, 200), 40, 40),
]

for i, enemy in enumerate(enemies):
    random_enemy = random.randrange(3)
    screen.blit(enemy_images[random_enemy], enemy)


# Fonts
font = pygame.font.Font(None, 36)

#control the amount of bullets per second
bullets_per_second = 15
timeAlfa = time.perf_counter()


# Main game loop
while not game_over:

    #draw top bar
    pygame.draw.rect(screen, BLACK, top_bar)
    player_name_surface = font.render(player_name, True, YELLOW)
    score_surface = font.render("Score: " + str(player_score), True, WHITE)

    screen.blit(player_name_surface, (20, 10))  # Adjust position as needed
    screen.blit(score_surface, (SCREEN_WIDTH - 150, 10))  # Adjust position as needed

    
    if new_game:
        # increase enemies
        enemies_number += 1
        # Restart  bullets
        bullets = []
        # restart enemies
        enemies = [pygame.Rect(random.randint(10, SCREEN_WIDTH - 10), random.randint(50, 200), 20, 20) for _ in range(enemies_number)]
        
        for i, enemy in enumerate(enemies):
            random_enemy = random.randrange(3)
            screen.blit(enemy_images[random_enemy], enemy)
            
        # wait for this game to end
        new_game = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_over = True

    if not game_over:
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            if cannon.x >=0 : 
               cannon.x -= CANNON_SPEED
               cannon_barrel.x -= CANNON_SPEED
        if keys[pygame.K_RIGHT]:
            if cannon.x <= 800:
               cannon.x += CANNON_SPEED
               cannon_barrel.x += CANNON_SPEED
        if keys[pygame.K_SPACE]:            
            timeBeta = time.perf_counter()
            if(timeBeta - timeAlfa >= bullets_per_second/100):
                timeAlfa = timeBeta
                bullet = pygame.Rect(cannon.centerx - 2, cannon.top, 4, 4)
                bullets.append(bullet)
                shoot_sound.play()

        # Update bullet positions
        bullets = [bullet for bullet in bullets if bullet.y > 0]
        for bullet in bullets:
            bullet.y -= BULLET_SPEED

        # Update enemy positions
        for enemy in enemies:
            enemy.y += ENEMY_SPEED

        # Check for player destruction
        for bullet in bullets:
            for enemy in enemies:
                if bullet.colliderect(enemy):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    player_score += 1 #increase score

        # Check if any enemy reached the bottom
        for enemy in enemies:
            if enemy.bottom >= SCREEN_HEIGHT:
                #game_over = True
                lose_sound.play()
                loser_message = font.render("You Lost!", True, RED)
                screen.blit(loser_message, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 18))
                pygame.display.flip()
                pygame.time.delay(2000)
                 # Wait for a key press to restart the game
                waiting_for_restart = True
                while waiting_for_restart:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                pygame.QUIT
                                game_over = True
                                waiting_for_restart = False
                            else:
                                waiting_for_restart = False     
                                new_game = True
                        if event.type == pygame.QUIT:
                            game_over = True
                            waiting_for_restart = False

        # Check if all enemies are destroyed
        if not enemies:
            win_sound.play()
            winner_message = font.render("Player  Wins!", True, GREEN)
            screen.blit(winner_message, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 18))
            pygame.display.flip()
            pygame.time.delay(2000)
            # Wait for a key press to restart the game
            waiting_for_restart = True
            while waiting_for_restart:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.QUIT
                            game_over = True
                            waiting_for_restart = False
                        else:
                            waiting_for_restart = False     
                            new_game = True
                    if event.type == pygame.QUIT:
                        game_over = True
                        waiting_for_restart = False

        # Clear the screen
        screen.fill(BLACK)
        
        screen.blit(background_image, (0,0))     
        
        #draw top bar
        pygame.draw.rect(screen, BLACK, top_bar)
        player_name_surface = font.render(player_name, True, YELLOW)
        score_surface = font.render("Score: " + str(player_score), True, WHITE)
    
        screen.blit(player_name_surface, (20, 10))  # Adjust position as needed
        screen.blit(score_surface, (SCREEN_WIDTH - 150, 10))  # Adjust position as needed
        
        # Draw cannon
        pygame.draw.rect(screen, GREEN, cannon)
        pygame.draw.rect(screen, GREEN, cannon_barrel)

        # Draw bullets
        for bullet in bullets:
            pygame.draw.rect(screen, WHITE, bullet)

        # Draw enemies     
        if enemies.count != 0:
            for i, enemy in enumerate(enemies):
                screen.blit(enemy_images[0], enemy)
            if(enemy_image_for_round == 3):
                enemy_image_for_round = 0 
            else:
                enemy_image_for_round += 1

        #draw top bar
        pygame.draw.rect(screen, BLACK, top_bar)                                                 
        
        # Update the display
        pygame.display.flip()

        # Control game speed (FPS)
        pygame.time.Clock().tick(60)
