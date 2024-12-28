import pygame
import time
import random

pygame.font.init()
pygame.mixer.init()

# Background music
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)


WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rain Dodging Simulator")

# Load and scale background image
BG = pygame.transform.scale(pygame.image.load("bg.jpg"), (WIDTH, HEIGHT))

# Player and rain properties
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VEL = 5

RAIN_WIDTH = 15
RAIN_HEIGHT = 20
RAIN_VEL = 4  # Initial velocity of raindrops

POWERUP_SIZE = 30
POWERUP_VEL = 3  # Speed of the power-up drop
INVINCIBILITY_DURATION = 2  # Duration of invincibility in seconds

# Font settings
FONT = pygame.font.SysFont("Times New Roman", 30)

# Function to draw the game elements
def draw(player, elapsed_time, drops, lives, powerups, invincible, invincible_start_time, warning_start_time):
    WIN.blit(BG, (0, 0))

    # Display elapsed time
    time_text = FONT.render(f"Time Elapsed: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    # Display remaining lives
    live_text = FONT.render(f"Lives Remaining: {lives}", 1, "white")
    WIN.blit(live_text, (WIDTH - live_text.get_width() - 10, 10))

    # Display invincibility status
    if invincible:
        invincible_text = FONT.render("INVINCIBLE!", 1, "yellow")
        WIN.blit(invincible_text, (WIDTH / 2 - invincible_text.get_width() / 2, 10))

    # Draw the player
    pygame.draw.rect(WIN, "green", player)

    # Draw the raindrops
    for rain in drops:
        pygame.draw.rect(WIN, "blue", rain)

    # Draw the power-ups
    for powerup in powerups:
        pygame.draw.rect(WIN, "gold", powerup)

    # Display warning text for 2 seconds
    if warning_start_time and time.time() - warning_start_time <= 2:
        warning_text = FONT.render("Watch out! Raindrops are faster!", 1, "red")
        text_x = WIDTH / 2 - warning_text.get_width() / 2  
        text_y = HEIGHT / 2 - warning_text.get_height() / 2  
        WIN.blit(warning_text, (text_x, text_y))


    pygame.display.update()

def main():
    global RAIN_VEL  
    run = True

    # Initialize player rectangle
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    # Initialize clock and timing
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    # Raindrop spawn 
    rain_add_increment = 2000
    rain_count = 0
    drops = []

    # Power Up Variables
    powerup_spawn_time = random.randint(10, 18)  
    powerups = []


    lives = 3
    invincible = False
    invincible_start_time = None

    warning_start_time = None

    while run:
        rain_count += clock.tick(60) 
        elapsed_time = time.time() - start_time


        if rain_count > rain_add_increment:
            for _ in range(5):
                rain_x = random.randint(0, WIDTH - RAIN_WIDTH)
                rain = pygame.Rect(rain_x, -RAIN_HEIGHT, RAIN_WIDTH, RAIN_HEIGHT)
                drops.append(rain)

            rain_add_increment = max(500, rain_add_increment - 100)
            if RAIN_VEL < 10:  
                RAIN_VEL += 0.5

            rain_count = 0

        if elapsed_time >= powerup_spawn_time:
            powerup_x = random.randint(0, WIDTH - POWERUP_SIZE)
            powerup = pygame.Rect(powerup_x, -POWERUP_SIZE, POWERUP_SIZE, POWERUP_SIZE)
            powerups.append(powerup)
            powerup_spawn_time += random.randint(5, 10) 


        if RAIN_VEL >= 8 and not warning_start_time:
            warning_start_time = time.time()  


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break


        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL

        for rain in drops[:]:
            rain.y += RAIN_VEL
            if rain.y > HEIGHT:
                drops.remove(rain)
            elif rain.y + rain.height >= player.y and rain.colliderect(player):
                if not invincible:  
                    drops.remove(rain)
                    lives -= 1
                    break


        for powerup in powerups[:]:
            powerup.y += POWERUP_VEL
            if powerup.y > HEIGHT:
                powerups.remove(powerup)
            elif powerup.colliderect(player):
                powerups.remove(powerup)
                invincible = True
                invincible_start_time = time.time()

        if invincible and time.time() - invincible_start_time >= INVINCIBILITY_DURATION:
            invincible = False


        if lives == 0:
            lost_text = FONT.render("YOU LOST!!", 1, "black")
            WIN.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, HEIGHT / 2 - lost_text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(3000)
            break


        draw(player, elapsed_time, drops, lives, powerups, invincible, invincible_start_time, warning_start_time)

    pygame.quit()


if __name__ == "__main__":
    main()
