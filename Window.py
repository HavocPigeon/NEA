from Mazes import *
from tkinter import *
import pygame

WALL_LIST = []#empty list to add the walls into

#pre-defining any colours that may be needed
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)

#constants for the screen size
SCREEN_WIDTH = 1340
SCREEN_HEIGHT = 710

def VizMaze(array, screen, wid, hei, end):#subroutine for drawing the maze and adding walls to the wall list
    screen.fill(WHITE)
    sqr = hei
    side = SCREEN_HEIGHT
    WALL_LIST = []

    pygame.draw.rect(screen, GREEN, end)#draws the exit of the maze

    if len(WALL_LIST) == 0:#if there is no walls it runs the code to populate the wall list
        for i in range(hei):
            for j in range(wid):#runs through all of the maze
                if array[i][j] == 0:#if it encounters a wall it adds it to the wall list
                    wall = pygame.Rect((j*SCREEN_WIDTH/len(array[0])/2), i*(SCREEN_HEIGHT/len(array)), side/sqr, (side/sqr)+1)#defines the wall with its location and size
                    WALL_LIST.append(wall)

    for item in WALL_LIST:
        pygame.draw.rect(screen, BLACK, item)#draws the walls
    
