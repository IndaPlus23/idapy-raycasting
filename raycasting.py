import pygame
import sys
import numpy as np
import math

# Initialize Pygame
pygame.init()

# Constants
width, height = 600, 400
fov = 60 #Players field of view
max_distance = 200 #Currently large than the biggest distance between the player and a wall
map_size = 5
map = np.array([
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1]
])

# Player variables
posx, posy = 1.5, 1.5
exitx, exity = 3, 3
rot = np.pi / 4
move_speed = 0.1
rotation_speed = np.pi / 30

#Set up pygame
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

def draw_fov(): #This function draws everything in the players field of vision

    for i in range(fov): #The field of veiw is 60 so there is 30 lines on each side of the player
        rot_i = rot + math.radians(i - fov / 2)
        x, y = posx, posy
        sin, cos = 0.02 * math.sin(rot_i), 0.02 * math.cos(rot_i)
        n = 0

        while True:
            x, y, n = x + cos, y + sin, n + 1
            if map[int(x)][int(y)] or n > max_distance:
                h = 1 / (0.02 * n)
                normalized_depth = n / max_distance
                color_depth = 1.0 - normalized_depth
                color = (255, int(255 * color_depth), int(255 * color_depth))
                break

        pygame.draw.line(screen, color, (i * (width / fov), height / 2 - h * height / 2),
                         (i * (width / fov), height / 2 + h * height / 2), 8)

        if i == 0 or i == fov - 1:
            pygame.draw.line(screen, (255, 255, 0), (i * (width / fov), height / 2),
                             (i * (width / fov), height / 2 + 0.6 * height / 2), 2)

while True:
    screen.fill((0, 0, 0))
    draw_fov()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        new_posx, new_posy = posx + move_speed * math.cos(rot), posy + move_speed * math.sin(rot)
        if map[int(new_posx)][int(new_posy)] == 0:
            posx, posy = new_posx, new_posy
    elif keys[pygame.K_s]:
        new_posx, new_posy = posx - move_speed * math.cos(rot), posy - move_speed * math.sin(rot)
        if map[int(new_posx)][int(new_posy)] == 0:
            posx, posy = new_posx, new_posy
    elif keys[pygame.K_a]:
        rot -= rotation_speed
    elif keys[pygame.K_d]:
        rot += rotation_speed
    elif keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()

    if map[int(posx)][int(posy)] == 0:
        if int(posx) == exitx and int(posy) == exity:
            font = pygame.font.Font(None, 36)
            text = font.render("You've reached the end of the maze!", True, (255, 255, 255))
            screen.blit(text, (width // 4, height // 2))
            pygame.display.flip()
            pygame.time.delay(1000)
            pygame.quit()
            sys.exit()

    pygame.display.flip()
    clock.tick(60)
