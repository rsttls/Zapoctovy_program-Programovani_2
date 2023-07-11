import pygame
import pygame.locals
import pygame.freetype
import time
import os
from collections import defaultdict


# game variables
width, height = 640, 480 # window size
cameraX, cameraY = 0, 0 # camera position
cameraSpeed = 0.5 # camera speed in pixel/milisecond
paused = 1 # if game is paused/unpaused
gridIsVisible = 1 # if grid is visible or not
mainLoopActive = 1 # if main loop is active
showHelp = 0 # 0 - stats + help, 1 - stats only, 2 - nothing

cyclePeriod = 500  # minimum time in miliseconds for one game cycle
fratetime = 16.666  # minimum time in miliseconds for one frame
lastCycletime = 0 # time mark
lastFrametime = 0 # time mark
timeMark = time.time_ns()/1000000 #time mark

fieldCurrent = defaultdict(lambda: defaultdict(int)) # main field of cells
fieldNew = defaultdict(lambda: defaultdict(int)) # new field of cells
checked = defaultdict(lambda: defaultdict(int)) # whether a cell in fieldCurrent has been check

# pygame variables
pygame.init()
pygame.display.set_caption("Game of life")
display = pygame.display.set_mode((width, height), pygame.RESIZABLE, vsync=1,)


# loads cell image and simplifies cell drawing
class cellSingleton:
    def __init__(self):
        self.image = pygame.image.load(os.path.dirname(__file__) + "/cell.png").convert_alpha()
        self.rect = self.image.get_rect()

    def draw(self, x, y):
        global display
        self.rect.x = x
        self.rect.y = y
        display.blit(self.image, self.rect)
cell = cellSingleton()





# loads grid image and simplifies grid drawing
class gridCellSingleton:
    def __init__(self):
        self.image = pygame.image.load(os.path.dirname(__file__) + "/grid.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def draw(self, x, y):
        global display
        self.rect.x = x
        self.rect.y = y
        display.blit(self.image, self.rect)
gridCell = gridCellSingleton()





# loads font and simplifies text drawing
class textSingleton:
    def __init__(self, color=(0, 0, 0)):
        self.font = pygame.freetype.Font(os.path.dirname(__file__) + "/Consolas.ttf", 17)
        self.color = color

    def draw(self, string, x, y):
        global display
        self.font.render_to(display, (x, y), string, self.color)
text = textSingleton((255, 255, 255))





# returns two intervals of visiable cells
def visiableCell():
    global cameraX, cameraY, width, height
    return ((int(cameraX) // 20), ((int(cameraX)+width) // 20)), ((int(cameraY) // 20), ((int(cameraY)+height) // 20))


# for cell at x,y count alive neighbors
def numberOfNeighbors(x, y):
    global fieldCurrent
    total = 0
    total += fieldCurrent[x-1][y-1]
    total += fieldCurrent[x][y-1]
    total += fieldCurrent[x+1][y-1]

    total += fieldCurrent[x-1][y]
    total += fieldCurrent[x+1][y]

    total += fieldCurrent[x-1][y+1]
    total += fieldCurrent[x][y+1]
    total += fieldCurrent[x+1][y+1]
    return total


# for cell at x,y applies rules
def applyLogic(x, y):
    global fieldCurrent, fieldNew
    if not checked[x][y]:
        checked[x][y] = 1
        if fieldCurrent[x][y] == 0:
            if numberOfNeighbors(x, y) == 3:
                fieldNew[x][y] = 1
        else:
            n = numberOfNeighbors(x, y)
            if n == 2 or n == 3:
                fieldNew[x][y] = 1


while mainLoopActive:
    # timing
    elapsed = (time.time_ns()/1000000) - timeMark
    timeMark = time.time_ns()/1000000
    # event
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            mainLoopActive = 0
        elif event.type == pygame.locals.VIDEORESIZE:
            width = display.get_width()
            height = display.get_height()
        # KEYDOWN input
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainLoopActive = 0
            elif event.key == pygame.K_e:
                cameraSpeed *= 1.5
            elif event.key == pygame.K_q:
                cameraSpeed *= 0.666
            elif event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_g:
                gridIsVisible = not gridIsVisible
            elif event.key == pygame.K_c:
                fieldCurrent.clear()
                paused = 1
            elif event.key == pygame.K_r:
                cameraX, cameraY = 0, 0
                cameraSpeed = 0.5
                cyclePeriod = 500
            elif event.key == pygame.K_x:
                cyclePeriod *= 0.75
            elif event.key == pygame.K_z:
                cyclePeriod *= 1.333
            elif event.key == pygame.K_h:
                showHelp = (showHelp+1)%3

    # continuous input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        cameraX -= cameraSpeed*elapsed
    if keys[pygame.K_s]:
        cameraY += cameraSpeed*elapsed
    if keys[pygame.K_d]:
        cameraX += cameraSpeed*elapsed
    if keys[pygame.K_w]:
        cameraY -= cameraSpeed*elapsed
    if paused:
        mouse = pygame.mouse.get_pressed()
        mousePos = pygame.mouse.get_pos()
        if mouse[0]:
            fieldCurrent[(mousePos[0]+int(cameraX)) //
                         20][(mousePos[1]+int(cameraY))//20] = 1
        elif mouse[2]:
            fieldCurrent[(mousePos[0]+int(cameraX)) //
                         20][(mousePos[1]+int(cameraY))//20] = 0


    # update
    if not paused:
        if timeMark - lastCycletime > cyclePeriod:
            lastCycletime = timeMark
            fieldNew.clear()
            checked.clear()
            # saves positions of all alive cells (all cell should be alive because in funtion applyLogic we access only alive cells)
            keyX = fieldCurrent.copy().keys()
            keyY = []
            for x in keyX:
                keyY.append(fieldCurrent[x].copy().keys())
            keyY.reverse()
            # iterating through all alive cells and checking all of their neighbors because if a dead cell becomes alive then it has at least one alive cell surrounding it
            for x in keyX:
                temp = keyY.pop()
                for y in temp:
                    if fieldCurrent[x][y]:
                        applyLogic(x-1, y-1)
                        applyLogic(x, y-1)
                        applyLogic(x+1, y-1)
                        applyLogic(x-1, y)
                        applyLogic(x, y)
                        applyLogic(x+1, y)
                        applyLogic(x-1, y+1)
                        applyLogic(x, y+1)
                        applyLogic(x+1, y+1)
            fieldCurrent, fieldNew = fieldNew, fieldCurrent

    #draw
    # FPS cap
    if timeMark - lastFrametime > fratetime:
        lastFrametime = timeMark
        # screen "refresh"
        display.fill((0, 0, 0))

        # draws grid
        if gridIsVisible:
            for x in range(0, (width+20)//gridCell.width+1):
                for y in range(0, (height+20)//gridCell.height+1):
                    gridCell.draw(x*gridCell.width - int(cameraX) %
                                  20, y*gridCell.height - int(cameraY) % 20)

        # draws visiable cells
        v = visiableCell()
        for x in range(v[0][0], v[0][1]+1):
            for y in range(v[1][0], v[1][1]+1):
                if fieldCurrent[x][y] == 1:
                    cell.draw(x*20 - int(cameraX), y*20 - int(cameraY))

        # draw text info
        if showHelp < 2:
            text.draw("Camera: " + str(cameraX) + ',' + str(cameraY), 10, 30)
            text.draw("Camera speed: " + str(cameraSpeed) + " px/ms", 10, 50)
            text.draw("Cycles per second: " + str(1000/cyclePeriod), 10, 70)
            if showHelp < 1:
                text.draw("wasd: camera movement" , 10 , 90)
                text.draw("space: pause/unpause simulation" , 10 , 110)
                text.draw("q/e: decrease/increase camera movement speed" , 10 , 130)
                text.draw("z/x: decrease/increase simulation speed" , 10 , 150)
                text.draw("c: kills all cells" , 10 , 170)
                text.draw("r: reset camera position, simulation and movement speed" , 10 , 190)
                text.draw("g: show/hide grid" , 10 , 210)
                text.draw("h: cycle through UI" , 10 , 230)
                text.draw("left mouse button: create cell (needs to be paused)" , 10 , 250)
                text.draw("right mouse button: kill cell (needs to be paused)" , 10 , 270)
                
        pygame.display.update()
