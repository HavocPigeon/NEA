from Window import *
import random
from enum import Enum
import numpy
import sys
import time

SCREEN_WIDTH = 1340
SCREEN_HEIGHT = 710
sys.setrecursionlimit(9999)
MAIN_SCREEN = pygame.display.set_mode((SCREEN_WIDTH//2, SCREEN_HEIGHT))#set up the window for the maze


class Neighbours(Enum):#Enumerator for constants for the directions
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class RDFS:
    def __init__(self, height, width, bias):
        '''
        for when the algorithm tries to check outside the array, it'll be viewing
        places that are outside the maze, but it will think they're visited cells
        To do this we make the maze an odd number and we will assign the outer cells
        to be visited
        '''
        if width % 2 == 0:
            width += 1
        if height % 2 == 0:
            height += 1
            
        self.width = width
        self.height = height
        self.__bias = bias

    def createMaze(self):
        maze = numpy.ones((self.height, self.width), dtype=float)#array full of ones, for the colour white, assigns them as float
        
        for i in range(self.height):
            for j in range(self.width):
                if int(i%2) == 1 or int(j%2) == 1:
                    maze[i, j] = 0 #walls, 0 for black
                if i == 0 or j == 0 or i == self.height - 1 or j == self.width - 1:
                    maze[i, j] = 0.5 #visited cells, 0.5 for grey

        sx = random.choice(range(2, self.width - 2, 2)) #starting cell
        sy = random.choice(range(2, self.height - 2, 2))

        self.Carve(sx, sy, maze)
        
        #make all cells white for being drawn
        for i in range(self.height):
            for j in range(self.width):
                if maze[i, j] == 0.5:
                    maze[i, j] = 1

   
        maze[1, 2] == 1 #start of the maze
        maze[self.height - 2, self.width - 3] = 1 #end of the maze

        return maze

                        
    def Carve(self, cx, cy, grid):
        grid[cy, cx] = 0.5 #assigns it as visited, cy and cx being the current coordinates
        ############################################################################################
        END_CELL = pygame.Rect((SCREEN_WIDTH//2)-((SCREEN_HEIGHT/self.height)*3)+2, SCREEN_HEIGHT-((SCREEN_HEIGHT/self.height)*2), SCREEN_HEIGHT/self.height, SCREEN_HEIGHT/self.height)
        VizMaze(grid, MAIN_SCREEN, self.width, self.height, END_CELL)
        pygame.display.update()
        time.sleep(0.01)
        ############################################################################################
        if (grid[cy - 2, cx] == 0.5 and grid[cy + 2, cx] and grid[cy, cx - 2] == 0.5 and grid[cy, cx + 2] == 0.5): #if all neighbours are visited
            pass
        else:
            nlist = [1,2,3,4]
            if self.__bias == 1:
                nlist.extend([3,4,3,4])
            elif self.__bias == 2:
                nlist.extend([1,2,1,2])
            while len(nlist) > 0:
                direction = random.choice(nlist)
                nlist.remove(direction)

                if direction == Neighbours.UP.value:
                    nx = cx #nx is next x coordinate
                    mx = cx #mx is the corresponding wall x coordinate
                    ny = cy - 2 #ny is the next y coordinate
                    my = cy - 1 #my is the corresponding wall y coordinate

                elif direction == Neighbours.DOWN.value:
                    nx = cx
                    mx = cx
                    ny = cy + 2
                    my = cy + 1

                elif direction == Neighbours.RIGHT.value:
                    nx = cx + 2
                    mx = cx + 1
                    ny = cy
                    my = cy

                elif direction == Neighbours.LEFT.value:
                    nx = cx - 2
                    mx = cx - 1
                    ny = cy
                    my = cy

                if grid[ny, nx] != 0.5:#if cell is unvisited
                    grid[my, mx] = 0.5#make the wall a passage
                    self.Carve(nx, ny, grid)#go to next cell
