import pygame
import os
import random 
import time

from pygame import MOUSEBUTTONDOWN
from pygame.examples import cursors

pygame.init()
pygame.mixer.init()  # Initialize the mixer module

# GLOBAL CONSTANTS
SCREENWIDTH = 1100
SCREENHEIGHT = 600
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

pygame.display.set_caption('Shinobi Dash')

# LOAD AND SCALE RUNNING IMAGES FOR THE NINJA CHARACTER
RUNNING = [pygame.transform.scale(pygame.image.load(os.path.join(".venv/Assets/Ninja", "ninja1.png")), (130, 130)),
           pygame.transform.scale(pygame.image.load(os.path.join(".venv/Assets/Ninja", "ninja2.png")), (130, 130))]

# LOAD AND SCALE JUMPING IMAGES FOR THE NINJA CHARACTER
JUMPING = [pygame.transform.scale(pygame.image.load(os.path.join(".venv/Assets/Ninja", "ninjaJump.png")), (130, 130)),
           pygame.transform.scale(pygame.image.load(os.path.join(".venv/Assets/Ninja", "ninjaJump2.png")), (130, 130))]

# LOAD AND SCALE DUCKING IMAGES FOR THE NINJA CHARACTER
DUCKING = [pygame.transform.scale(pygame.image.load(os.path.join(".venv/Assets/Ninja", "ninjaDuck1.png")), (119, 100)),
           pygame.transform.scale(pygame.image.load(os.path.join(".venv/Assets/Ninja", "ninjaDuck2.png")), (119, 100))]

# LOAD THE BACKGROUND AND GROUND IMAGES
BACKGROUND = pygame.image.load(os.path.join(".venv/Assets/Ninja", "background.jpg"))
GROUND = pygame.image.load(os.path.join(".venv/Assets/Ninja", "ground.png"))
CLOUDS = pygame.image.load(os.path.join(".venv/Assets/Ninja", "Clouds.png"))
SUN_IMG = pygame.transform.scale(pygame.image.load(os.path.join(".venv/Assets/Ninja", "sun.png")), (300, 300))

# Load the shuriken image
SHURIKEN_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join(".venv/Assets/Ninja", "shuriken1.png")), (50, 30))
KUNAI_IMG = pygame.transform.scale(pygame.image.load(os.path.join(".venv/Assets/Ninja", "kunai.png")), (120, 20))

LOGO = pygame.transform.scale(pygame.image.load(os.path.join(".venv/Assets/Ninja", "Logo.png")), (675, 375))
# Load font for Game Over text
FONT = pygame.font.SysFont('comicsans', 40)
JUMP_HIGH = 8.5

# Load sound effects and background music
JUMP_SOUND = pygame.mixer.Sound(os.path.join(".venv/Assets/SoundEffect", "slideClick.mp3"))
DUCK_SOUND = pygame.mixer.Sound(os.path.join(".venv/Assets/SoundEffect", "woosh.mp3"))
SHURIKEN_SOUND = pygame.mixer.Sound(os.path.join(".venv/Assets/SoundEffect", "woosh.mp3"))

# Load game over sound
GAME_OVER_SOUND = pygame.mixer.Sound(os.path.join(".venv/Assets/Music", "thrash.mp3"))

# Load background music track
BACKGROUND_MUSIC = os.path.join(".venv/Assets/Music", "knight.mp3")

def play_background_music():
    GAME_OVER_SOUND.stop()  # Stop the game over music
    pygame.mixer.music.stop()  # Stop any currently playing music
    pygame.mixer.music.load(BACKGROUND_MUSIC)
    pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely

def play_game_over_sound():
    pygame.mixer.music.stop()  # Stop the background music
    GAME_OVER_SOUND.play()

# Play the background music at the start
play_background_music()

class Ninja:
    def __init__(self):
        self.x_pos = 80
        self.y_pos = 325
        self.y_pos_duck = 355
        self.jump_vel = JUMP_HIGH

        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING
        self.ninja_duck = False
        self.ninja_run = True
        self.ninja_jump = False
        self.step_index = 0
        self.image = self.run_img[0]
        self.ninja_rect = self.image.get_rect()
        self.ninja_rect.x = self.x_pos
        self.ninja_rect.y = self.y_pos
        self.gravity = 0.8

    def update(self, userInput):
        if self.ninja_duck:
            self.duck()
        if self.ninja_run:
            self.run()
        if self.ninja_jump:
            self.jump()

        if userInput[pygame.K_LEFT]:
            self.ninja_rect.x -= 10
        if userInput[pygame.K_RIGHT]:
            self.ninja_rect.x += 10

        if self.ninja_rect.x < 0:
            self.ninja_rect.x = 0
        if self.ninja_rect.x > SCREENWIDTH - self.ninja_rect.width:
            self.ninja_rect.x = SCREENWIDTH - self.ninja_rect.width

        if userInput[pygame.K_UP] and self.ninja_rect.y == self.y_pos:
            self.ninja_duck = False
            self.ninja_run = False
            self.ninja_jump = True
            self.jump_vel = JUMP_HIGH
            JUMP_SOUND.play()  # Play jump sound
        elif userInput[pygame.K_SPACE] and self.ninja_rect.y == self.y_pos:
            self.ninja_duck = False
            self.ninja_run = False
            self.ninja_jump = True
            self.jump_vel = JUMP_HIGH
            JUMP_SOUND.play()  # Play jump sound

        elif userInput[pygame.K_DOWN] and not self.ninja_jump:
            self.ninja_duck = True
            self.ninja_run = False
            self.ninja_jump = False
            DUCK_SOUND.play()  # Play duck sound
        elif not (self.ninja_jump or userInput[pygame.K_DOWN]):
            self.ninja_duck = False
            self.ninja_run = True
            self.ninja_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.step_index += 1
        if self.step_index >= 10:
            self.step_index = 0
        self.ninja_rect.y = self.y_pos_duck

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.step_index += 1
        if self.step_index >= 10:
            self.step_index = 0
        self.ninja_rect.y = self.y_pos

    def jump(self):
        if self.ninja_jump:
            if self.jump_vel > 0:
                self.image = self.jump_img[0]
            else:
                self.image = self.jump_img[1]

            self.ninja_rect.y -= self.jump_vel * 4
            self.jump_vel -= self.gravity
            if self.ninja_rect.y >= self.y_pos:
                self.ninja_rect.y = self.y_pos
                self.ninja_jump = False
                self.jump_vel = JUMP_HIGH

    def auto_play(self):
        if not self.ninja_jump and random.randint(0, 20) == 0:
            self.ninja_jump = True
            self.jump_vel = JUMP_HIGH
            JUMP_SOUND.play()  # Play jump sound

        if self.ninja_jump:
            self.jump()
        else:
            self.run()

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.ninja_rect.x, self.ninja_rect.y))

class Shuriken:
    def __init__(self):
        self.image = SHURIKEN_IMAGE
        self.rect = self.image.get_rect()
        self.rect.x = SCREENWIDTH
        self.rect.y = random.randint(100, SCREENHEIGHT - 150)
        self.speed = 10

    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < -self.rect.width:
            self.rect.x = SCREENWIDTH
            self.rect.y = random.randint(100, SCREENHEIGHT - 150)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))

class Kunai:
    def __init__(self):
        self.image = KUNAI_IMG
        self.rect = self.image.get_rect()
        self.rect.x = SCREENWIDTH
        self.rect.y = random.randint(100, SCREENHEIGHT - 150)
        self.speed = 20

    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < -self.rect.width:
            self.rect.x = SCREENWIDTH
            self.rect.y = random.randint(100, SCREENHEIGHT - 150)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))

def draw_background(SCREEN, bg_x):
    SCREEN.blit(BACKGROUND, (bg_x, 0))
    SCREEN.blit(BACKGROUND, (bg_x + BACKGROUND.get_width(), 0))

def draw_ground(SCREEN, ground_x, ground_y):
    SCREEN.blit(GROUND, (ground_x, ground_y))
    SCREEN.blit(GROUND, (ground_x + GROUND.get_width(), ground_y))

def draw_clouds(SCREEN, cloud_x, cloud_y):
    SCREEN.blit(CLOUDS, (cloud_x, cloud_y))
    SCREEN.blit(CLOUDS, (cloud_x + CLOUDS.get_width(), cloud_y))

def draw_sun(SCREEN):
    SCREEN.blit(SUN_IMG, (SCREENWIDTH // 2 - 200, SCREENHEIGHT // 2 - 125))

def draw_game_over(SCREEN):
    game_over_text = FONT.render('                ', True, (255, 0, 0))
    restart_button_text = FONT.render('Press Enter', True, (0, 0, 0))
    restart_button = pygame.Rect(SCREENWIDTH // 2 - 125, SCREENHEIGHT // 2 + 100, 250, 50)
    pygame.draw.rect(SCREEN, (250, 250, 250), restart_button)
    SCREEN.blit(game_over_text, (SCREENWIDTH // 2 - game_over_text.get_width() // 2, (SCREENHEIGHT // 2) + 75 - game_over_text.get_height() // 2))
    SCREEN.blit(restart_button_text, (SCREENWIDTH // 2 - restart_button_text.get_width() // 2, (SCREENHEIGHT // 2) + 120 - restart_button_text.get_height() // 2))
    return restart_button

def main():
    run = True
    game_over = False
    clock = pygame.time.Clock()
    player = Ninja()
    shuriken = Shuriken()
    kunai = Kunai()
    elapsed_time = 0
    score = 0  # Initialize score
    best_time = 0  # Initialize best time

    bg_x = 0
    ground_x = 0
    ground_y = player.y_pos + 123
    cloud_x = 0
    cloud_y = player.y_pos - 300

    game_over_time = None
    game_over_pause_duration = 1000  # 1 second

    initial_shuriken_speed = shuriken.speed
    initial_background_speed = 2
    initial_ground_speed = 6
    initial_clouds_speed = 4

    shuriken_speed = initial_shuriken_speed
    background_speed = initial_background_speed
    ground_speed = initial_ground_speed
    cloud_speed = initial_clouds_speed

    last_speed_increase_time = time.time()
    start_time = time.time()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if game_over and event.type == pygame.MOUSEBUTTONDOWN and restart_button.collidepoint(event.pos):
                game_over = False
                player = Ninja()
                shuriken = Shuriken()
                kunai = Kunai()
                bg_x = 0
                ground_x = 0
                cloud_x = 0
                game_over_time = None
                play_background_music()
                shuriken_speed = initial_shuriken_speed
                background_speed = initial_background_speed
                ground_speed = initial_ground_speed
                cloud_speed = initial_clouds_speed
                start_time = time.time()
                score = 0  # Reset score

            if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_over = False
                player = Ninja()
                shuriken = Shuriken()
                kunai = Kunai()
                bg_x = 0
                ground_x = 0
                cloud_x = 0
                game_over_time = None
                play_background_music()
                shuriken_speed = initial_shuriken_speed
                background_speed = initial_background_speed
                ground_speed = initial_ground_speed
                cloud_speed = initial_clouds_speed
                start_time = time.time()
                score = 0  # Reset score

        if not game_over:
            draw_background(SCREEN, bg_x)
            draw_ground(SCREEN, ground_x, ground_y)
            draw_sun(SCREEN)  # Draw the sun
            draw_clouds(SCREEN, cloud_x, cloud_y)

            userInput = pygame.key.get_pressed()

            bg_x -= background_speed
            ground_x -= ground_speed
            cloud_x -= cloud_speed

            if bg_x <= -BACKGROUND.get_width():
                bg_x = 0
            if ground_x <= -GROUND.get_width():
                ground_x = 0
            if cloud_x <= -CLOUDS.get_width():
                cloud_x = 0

            player.update(userInput)
            player.draw(SCREEN)

            shuriken.update()
            shuriken.draw(SCREEN)
            if player.ninja_rect.colliderect(shuriken.rect):
                game_over = True
                game_over_time = pygame.time.get_ticks()
                play_game_over_sound()

            current_time = time.time()
            if current_time - last_speed_increase_time >= 3:
                shuriken_speed *= 1.1
                background_speed *= 1.1
                ground_speed *= 1.1
                cloud_speed *= 1.1
                last_speed_increase_time = current_time

            elapsed_time = time.time() - start_time
            score = int(elapsed_time)  # Update score based on elapsed time

            if elapsed_time >= 10:
                kunai.update()
                kunai.draw(SCREEN)
            if player.ninja_rect.colliderect(kunai.rect):
                game_over = True
                game_over_time = pygame.time.get_ticks()
                play_game_over_sound()

            # Calculate elapsed time in milliseconds
            elapsed_time_ms = (time.time() - start_time) * 1000

            # Display the timer in milliseconds
            timer_text = FONT.render(f'Score: {int(elapsed_time_ms)}', True, (0, 0, 0))
            SCREEN.blit(timer_text, (10, 10))  # Display the timer at the top-left corner

        if game_over:
            if pygame.time.get_ticks() - game_over_time <= game_over_pause_duration:
                pygame.time.wait(game_over_pause_duration)

            # Update best time if the current elapsed time is greater than the best time
            if elapsed_time_ms > best_time:
                best_time = elapsed_time_ms

            bg_x -= background_speed
            ground_x -= ground_speed
            cloud_x -= cloud_speed

            if bg_x <= -BACKGROUND.get_width():
                bg_x = 0
            if ground_x <= -GROUND.get_width():
                ground_x = 0
            if cloud_x <= -CLOUDS.get_width():
                cloud_x = 0

            draw_background(SCREEN, bg_x)
            draw_ground(SCREEN, ground_x, ground_y)

            # Draw the logo image
            logo_x = 220
            logo_y = 70
            SCREEN.blit(LOGO, (logo_x, logo_y))

            player.auto_play()
            player.draw(SCREEN)

            shuriken.update()
            shuriken.draw(SCREEN)

            restart_button = draw_game_over(SCREEN)

            # Display the best time on the game over screen, positioned 10 pixels below the restart button
            best_time_text = FONT.render(f'Highest Score: {int(best_time)}', True, (255, 255, 255))
            SCREEN.blit(best_time_text, (SCREENWIDTH // 2 - best_time_text.get_width() // 2, SCREENHEIGHT // 2 + restart_button.height + 100))

            timer_text = FONT.render(f'Score: {int(elapsed_time_ms)}', True, (0, 0, 0))
            SCREEN.blit(timer_text, (10, 10))  # Display the timer at the top-left corner

        clock.tick(30)
        pygame.display.update()

    pygame.quit()#quit

main()
