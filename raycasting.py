import numpy as np
from matplotlib import pyplot as plt
import keyboard

map = [[1, 1, 1, 1, 1], #Test map
        [1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1]]

posx, posy, rot = 1.5, 1.5, np.pi / 4 #Starting position
exitx, exity = 3, 3 #The exit

while 1:
    for i in range(60): #The vision is 60 degrees
        rot_i = rot + np.deg2rad(i - 30) #The first line is at 30 degrees to the left of the player
        x, y = posx, posy
        sin, cos = 0.02 * np.sin(rot_i), 0.02 * np.cos(rot_i)
        n = 0

        while True: #This is the ray that will stop when it finds a wall and draw a line depending on how long the ray was.
            x, y, n = x + cos, y + sin, n + 1
            if map[int(x)][int(y)]:
                h = 1 / (0.02 * n)
                depth = 1.0 - 0.25 * (n / 60.0)
                color = (1.0, 0.5*depth, 0.8*depth)
                break

        plt.vlines(i, -h, h, color= color, lw=8)

    plt.axis('off')
    plt.tight_layout()
    plt.axis((0, 60, -1, 1))
    plt.draw()
    plt.pause(0.0001)
    plt.clf()

    key = keyboard.read_key()
    x, y = (posx, posy)

    if key == 'w':
        x, y = (x + 0.3 * np.cos(rot), y + 0.3 * np.sin(rot))
    elif key == 's':
        x, y = (x - 0.3 * np.cos(rot), y - 0.3 * np.sin(rot))
    elif key == 'a':
        rot = rot - np.pi / 10
    elif key == 'd':
        rot = rot + np.pi / 10
    elif key == 'esc':
        break

    if map[int(x)][int(y)] == 0: #The program is a maze and if the player reaches the exit the program exits.
        if int(posx) == exitx and int(posy) == exity:

            plt.text(0.1, 0.5, "You've reached the end of the maze!", fontsize=20, color='black')
            plt.show(block=False)
            plt.pause(2)
            break

        posx, posy = (x, y)

plt.close()