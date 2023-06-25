from Mazes import *
from Window import *
from tkinter import *
import pygame
from pygame.locals import *
import sys
import time

#opens the file for the scores
try:
    file = open("MazeTimes.txt", "r")
except FileNotFoundError:
    file = open("MazeTimes.txt", "w")
    file.close()
    file = open("MazeTimes.txt", "r")

timeArray = []#empty array to be populated by the scores


for line in file:#populates the array
    timeArray.append(line)
    if len(timeArray) > 1:
        break

file.close()
    
pygame.init()
pygame.font.init()

MY_FONT = pygame.font.SysFont("Comic Sans MS", 15)#font to display scores

#pre-defined colours
BLACK = (0,0,0)
GREY = (127,127,127)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)



#screen size constants
SCREEN_WIDTH = 1340
SCREEN_HEIGHT = 710

class Player:
    def __init__(self, x, y, wid, hei):
        self.x = x#current player coordinates
        self.y = y
        self.px = self.x#previous player coordinates
        self.py = self.y
        self.width = wid#player size
        self.height = hei
        self.character = pygame.Rect(self.x, self.y, self.width, self.height)#defines the player

    def collisionDetection(self, array):
        press_key = pygame.key.get_pressed()
        if press_key[K_q]:
            return True
        if len(self.character.collidelistall(array)) == 0:#checks a list of all objects in an array which collide with the player
            return True#if there is nothing colliding with the player then it returns Return
        else:
            return False
            

    def Victory(self, end):
        if self.character.colliderect(end):#checks if the player is colliding with the exit of the maze
            return False
        else:
            return True
        

    def move(self, key, array):

        speed = self.width/35
        press_key = pygame.key.get_pressed()
        if press_key[K_c]:
            speed = 0.07
        if press_key[K_v]:
            speed *= 1.5
        
        if self.collisionDetection(array):#if there is nothing colliding with the player
            if key[K_w]:
                self.py = self.y
                self.y -= speed
            if key[K_a]:
                self.px = self.x
                self.x -= speed
            if key[K_s]:
                self.py = self.y
                self.y += speed
            if key[K_d]:
                self.px = self.x
                self.x += speed
            else:
                self.x += 0
                self.y += 0

            self.character = pygame.Rect(self.x, self.y, self.width, self.height)

            if self.collisionDetection(array):#if there is nothing colliding with the new position of the player
                pass
            else:#if the new position is colliding with a wall, it puts the player to its previous position
                self.x = self.px
                self.y = self.py
                self.character = pygame.Rect(self.x, self.y, self.width, self.height)

        
        else:
            self.x = self.px
            self.y = self.py
            
            
            self.character = pygame.Rect(self.x, self.y, self.width, self.height)


    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.character)#draws the player

    

root = Tk()#initiates the window for tkinter
SliderLabel = Label(root, text="Side Length:")
InsLabel = Label(root, text="Instructions:")
Instructions = Label(root, text="Use the w,a,s,d keys to move the player.\nYou can use the c key to move\nthe player slower for more precise movement.\nYou can use the v key to move the player faster.\nYou must guide your red player character\nto the exit of the maze,\nwhich is marked with a green square.")
Slider = Scale(root, from_=20, to=100, orient=HORIZONTAL, tickinterval=1, sliderlength=7)#entry for users to input the side length of the maze
variable2 = StringVar(root)
algList = OptionMenu(root, variable2, "Unbiased", "Horizontal", "Vertical")#drop-down menu for the algorithms

def GameLoop(array, maze, character, end):#subroutine for running the game
    root.destroy()#closes the tkinter window
    MAIN_SCREEN.fill(GREY)
    #time.sleep(10)
    START_TIME = round(time.time(), 2)#start time to count from for the timer
    TOTAL_TIME = None

    while character.Victory(end):#while the player is not at the end, enter the game loop
        TOTAL_TIME = round((time.time() - START_TIME), 2)#calculates current time
        MAIN_SCREEN.fill(WHITE)
        TEXT_SURFACE = MY_FONT.render(f"{TOTAL_TIME}", False, (255, 0, 0))#defines the timer
        
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit

        pressed_keys = pygame.key.get_pressed()
                
        VizMaze(array, MAIN_SCREEN, maze.width, maze.height, end)#passes the maze through to the drawing subroutine
        character.move(pressed_keys, WALL_LIST)
        character.draw(MAIN_SCREEN)
        MAIN_SCREEN.blit(TEXT_SURFACE, (0,0))
        pygame.display.update()
        
    MAIN_SCREEN.fill(BLACK)

    #code for displaying the current time
    currentTime = MY_FONT.render(f"Current Time: {TOTAL_TIME}", False, (WHITE))
    currTimeRect = currentTime.get_rect()
    currTimeRect.center = (SCREEN_WIDTH//4, (SCREEN_HEIGHT//2)-50)
    MAIN_SCREEN.blit(currentTime, currTimeRect)

    #code for displaying the high score
    highscoreTime = MY_FONT.render(f"High Score: {timeArray[0]}", False, (WHITE))
    highscoreRect = highscoreTime.get_rect()
    highscoreRect.center = (SCREEN_WIDTH//4, SCREEN_HEIGHT//2)
    MAIN_SCREEN.blit(highscoreTime, highscoreRect)

    #code for displaying the previous time
    prevTime = MY_FONT.render(f"Previous Score: {timeArray[1]}", False, (WHITE))
    prevTimeRect = prevTime.get_rect()
    prevTimeRect.center = (SCREEN_WIDTH//4, (SCREEN_HEIGHT//2)+50)
    MAIN_SCREEN.blit(prevTime, prevTimeRect)

    timeArray[1] = TOTAL_TIME#updates the previous time to be added to the file of scores

    pygame.display.update()

    if TOTAL_TIME < float(timeArray[0]):#if the new time is better than the high score
        timeArray[0] = TOTAL_TIME#makes it the new high score

    file = open("MazeTimes.txt", "w")#open score file

    for item in timeArray:
        file.write(f"{str(item)}")#write the scores back to the file

    file.close()#close file
        

def GetSettings():
    side = Slider.get()#get parameters for the maze
    alg = variable2.get()
    MAIN_SCREEN = pygame.display.set_mode((SCREEN_WIDTH//2, SCREEN_HEIGHT))
    MAIN_SCREEN.fill(WHITE)
    if alg == "Unbiased":
        newMaze = RDFS(int(side), int(side), 0)#initialise the algorithm
        mazeArray = newMaze.createMaze()#create the maze
        player = Player((SCREEN_HEIGHT/newMaze.height)*2, ((SCREEN_HEIGHT/newMaze.height)+1)*2, (SCREEN_HEIGHT/newMaze.height)-4, (SCREEN_HEIGHT/newMaze.height)-4)#initialise the player
        END_CELL = pygame.Rect((SCREEN_WIDTH//2)-((SCREEN_HEIGHT/newMaze.height)*3)+2, SCREEN_HEIGHT-((SCREEN_HEIGHT/newMaze.height)*2), SCREEN_HEIGHT/newMaze.height, SCREEN_HEIGHT/newMaze.height)#initialise the exit of the maze
        VizMaze(mazeArray, MAIN_SCREEN, newMaze.width, newMaze.height, END_CELL)
        GameLoop(mazeArray, newMaze, player, END_CELL)#enter the game loop
    elif alg == "Horizontal":
        newMaze = RDFS(int(side), int(side), 1)#initialise the algorithm
        mazeArray = newMaze.createMaze()#create the maze
        player = Player((SCREEN_HEIGHT/newMaze.height)*2, ((SCREEN_HEIGHT/newMaze.height)+1)*2, (SCREEN_HEIGHT/newMaze.height)-4, (SCREEN_HEIGHT/newMaze.height)-4)#initialise the player
        END_CELL = pygame.Rect((SCREEN_WIDTH//2)-((SCREEN_HEIGHT/newMaze.height)*3)+2, SCREEN_HEIGHT-((SCREEN_HEIGHT/newMaze.height)*2), SCREEN_HEIGHT/newMaze.height, SCREEN_HEIGHT/newMaze.height)#initialise the exit of the maze
        VizMaze(mazeArray, MAIN_SCREEN, newMaze.width, newMaze.height, END_CELL)
        GameLoop(mazeArray, newMaze, player, END_CELL)#enter the game loop
    elif alg == "Vertical":
        newMaze = RDFS(int(side), int(side), 2)#initialise the algorithm
        mazeArray = newMaze.createMaze()#create the maze
        player = Player((SCREEN_HEIGHT/newMaze.height)*2, ((SCREEN_HEIGHT/newMaze.height)+1)*2, (SCREEN_HEIGHT/newMaze.height)-4, (SCREEN_HEIGHT/newMaze.height)-4)#initialise the player
        END_CELL = pygame.Rect((SCREEN_WIDTH//2)-((SCREEN_HEIGHT/newMaze.height)*3)+2, SCREEN_HEIGHT-((SCREEN_HEIGHT/newMaze.height)*2), SCREEN_HEIGHT/newMaze.height, SCREEN_HEIGHT/newMaze.height)#initialise the exit of the maze
        VizMaze(mazeArray, MAIN_SCREEN, newMaze.width, newMaze.height, END_CELL)
        GameLoop(mazeArray, newMaze, player, END_CELL)#enter the game loop
    

button = Button(root, text="Draw Maze", command=GetSettings)#button to draw the maze

SliderLabel.grid(row=0, column=0)
Slider.grid(row=0, column=1)

variable2.set("Unbiased")#default maze generation algorithm is recursive backtracking

InsLabel.grid(row=3, column=0)
Instructions.grid(row=4, column=1)

algList.grid(row=2, column=1)

button.grid(row=3, column=1)

MAIN_SCREEN = pygame.display.set_mode((SCREEN_WIDTH//2, SCREEN_HEIGHT))#set up the window for the maze
