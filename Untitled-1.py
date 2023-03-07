#TODO: put imports under this line
from cmath import nan
from os import scandir
import random
from shutil import move
from tkinter import N
import pygame
import sys
import OpenGL

#TODO: Move variables under this line
#make window resizable

#print hello world 10 times
#TODO: genrate function to print "hello world" x times
def PforX(x):
    for i in range(x): 
        print("hello world")
#open new window, display a 6 sided cube
#todo: generate a function to display a 6 sided cube


#define player movemnt via key presess


def renderLoop():
    screen = pygame.display.set_mode((32 * 32, 32 * 32), pygame.RESIZABLE)
    oldsize = screen.get_size()
    position = nan
    oldsize = (32 * 32, 32 * 32)
    #ToDo: generate premade tile map 32x32 vith random colors
    tileMap = [[(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for x in range(32)] for y in range(32)]
    ntileMap = [[(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for x in range(32)] for y in range(32)]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.fill((0, 0, 0))
        
        #TODO: generate circle at position of a variable, update variable based on w a s d key presses
        #TODO: translate position to screen coordinates and convert to float make new float object and set cordinates individualy without subscripting
        positionn = (float(0), float(0))
        pygame.draw.circle(screen, (255, 255, 255), positionn , 10)

        #detect a screen resize with old screen size stored a "oldsize" variable
        if oldsize != screen.get_size():
            tileMap = [[(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for x in range(int(screen.get_width()/32))] for y in range(int(screen.get_height()/32))]
            ntileMap = tileMap
            oldsize = screen.get_size()
            print(oldsize)
        else:
            tileMap = ntileMap

        


        




        #fix code to not do anything if index is out of range
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x = pos[0] // 32
            y = pos[1] // 32
            tileMap[y][x] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        #change tile color for touch event

        #fix tile rendering for resizable screen   
        for y in range(len(tileMap)):
            for x in range(len(tileMap[y])):
                pygame.draw.rect(screen, tileMap[y][x], (x * 32, y * 32, 32, 32))
        pygame.display.update()
        pygame.time.Clock().tick(60)
    pygame.quit()
    quit()
#TODO: initialize render loop, openGL, openAL
def init():
    position = [0 , 0]
    #openGL stuff RIP
    #openAL stuff
    #pygame.mixer.init()
    #TODO: get music from youtube
    #pygame.mixer.music.load("music.mp3")
   # pygame.mixer.music.play(-1)
    pygame.init()
    pygame.display.set_caption("some game")
    position = (0, 0)



if __name__ == "__main__":
    PforX(10)
    print("im main")
    init()
    renderLoop()




