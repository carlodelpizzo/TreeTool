import pygame
from pygame.locals import *


pygame.init()
clock = pygame.time.Clock()
frame_rate = 60
# Screen
screen_width = 500
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
# Title
pygame.display.set_caption('Decision Tree Tool')
# Colors
black = [0, 0, 0]
white = [255, 255, 255]
red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]
grid_color = [50, 50, 50]
# Font
font_size = 25
font_face = "Helvetica"
main_font = pygame.font.SysFont(font_face, font_size)


running = True
while running:
    screen.fill(black)
    # Event loop
    for event in pygame.event.get():
        # Close window
        if event.type == pygame.QUIT:
            running = False
            break

        # Key down events
        keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:
            # Close window shortcut
            if (keys[K_LCTRL] or keys[K_RCTRL]) and keys[K_w]:
                running = False
                break

        # Key up events
        if event.type == pygame.KEYUP:
            pass

    clock.tick(frame_rate)
    pygame.display.flip()


pygame.display.quit()
pygame.quit()
