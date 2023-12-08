import pygame
import sys
import numpy as np
import math

# Initialize Pygame
pygame.init()

# Constants
width, height = 600, 400
fov = 60 #Players field of view
max_distance = 275 #Currently large than the biggest distance between the player and a wall
map_size = 7
map = np.array([
    [1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1]
])

# Player variables
posx, posy = 1.5, 1.5
exitx, exity = 5, 5
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
            x, y, n = x + cos, y + sin, n + 1 #Casting the ray

            if map[int(x)][int(y)] or n > max_distance: #When we hit a wall or reach the max distance
                h = 1 / (0.02 * n) #This is the height of the wall. It depends on the distance to the player.

                #These decide the color. Also depending on the distance to the player.
                normalized_depth = n / max_distance
                color_depth = 1.0 - normalized_depth
                color = (255, int(255 * color_depth), int(255 * color_depth))
                break

    #Draws a line that is perfectly mirrored in the x axis and depends on the length to the wall. 10 makes the wall solid
        pygame.draw.line(screen, color, (i * (width / fov), height / 2 - h * height / 2),
                         (i * (width / fov), height / 2 + h * height / 2), 10)



def show_minimap():
    minimap = pygame.Surface((width, height))
    minimap.fill((255, 255, 255)) #The minimap starts off completely white

    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            if map[i][j] == 1: #If there is a wall we draw a rectangle there
                pygame.draw.rect(minimap, (0, 0, 0), (j * (width / map_size), i * (height / map_size),
                                                    width / map_size, height / map_size))
                #Color the exit red
            elif i == exitx and j == exity:
                pygame.draw.rect(minimap, (255, 0, 0), (j * (width / map_size), i * (height / map_size),
                                                    width / map_size, height / map_size))

    #Draw a circle at the position of the player
    pygame.draw.circle(minimap, (255, 0, 0), (int(posy * (width / map_size)), int(posx * (height / map_size))), 10)

    #Maps out a line for the way the player is looking. This is the center of the filed of view
    fov_line_start = (
        int(posy * (width / map_size)),
        int(posx * (height / map_size))
    )
    fov_line_end = (
        int((posy + math.sin(rot)) * (width / map_size)),
        int((posx + math.cos(rot)) * (height / map_size))
    )

    #Draws the line
    pygame.draw.line(minimap, (255, 255, 0), fov_line_start, fov_line_end, 2)

    screen.blit(minimap, (0, 0))
    pygame.display.flip()


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
    elif keys[pygame.K_m]:
        show_minimap()


    #If we reach the exit of the map we show a text telling the player they found the exit
    if map[int(posx)][int(posy)] == 0:
        if int(posx) == exitx and int(posy) == exity:
            font = pygame.font.Font(None, 40)
            text = font.render("You've reached the end of the maze!", True, (0, 0, 255))
            screen.blit(text, (width // 6, height // 4))
            pygame.display.flip()
            pygame.time.delay(1000)
            pygame.quit()
            sys.exit()

    pygame.display.flip()
    clock.tick(60)
