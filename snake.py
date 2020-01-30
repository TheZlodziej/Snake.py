from array import *
import pygame
import random

pygame.init()
    
#window setup
windowW = 600
windowH = 600
windowTitle = "Snake.py"

window = pygame.display.set_mode((windowW, windowH))
pygame.display.set_caption(windowTitle)

# 0 = empty
# 1 = snake
# 2 = apple

segmentWidth = 20
segmentHeight = 20

mapWidth = (int)(windowW / segmentWidth)
mapHeight = (int)(windowH / segmentHeight)
mapColor = (255, 255, 255)
map = []

for y in range(0, mapHeight):
    row = []
    for x in range(0, mapWidth):
        row.append(0)

    map.append(row)

#snake setup
speed = 0.05 #speed * 1000 [ms]
direction = (1, 0) # (x, y) # 1, 0 = right; -1, 0 = left; 0, 1 = down; 0, -1 = bottom #
alive = True
snakeBody = [(2,0), (1,0), (0,0)] # (x, y)
snakeColor = (0, 255, 0)

#apple setup
def spawnApple():
    global mapHeight, mapWidth, snakeBody, alive, map
    available = []
    
    for y in range(0, mapHeight-1):
        for x in range(0, mapWidth-1):
            for el in snakeBody:
                if not el == (x, y):
                    available.append((x,y))

    if len(available) > 0:
        newApple = random.choice(available)
        map[newApple[1]][newApple[0]] = 2
        return newApple
    
    else:
        alive = False

apple = spawnApple()
appleColor = (255, 0, 0)

def updateMap():
    global mapHeight, mapWidth, segmentHeight, segmentWidth, window, snakeColor, mapColor, appleColor

    for i in range(0, mapHeight): # for every Y
        for j in range(0, mapWidth): # for every X
            if map[i][j] == 0:
                #map
                pygame.draw.rect(window, mapColor, (j*segmentWidth, i*segmentHeight, segmentWidth, segmentHeight))

            if map[i][j] == 1:
                #snake
                pygame.draw.rect(window, snakeColor, (j*segmentWidth, i*segmentHeight, segmentWidth, segmentHeight))

            if map[i][j] == 2:
                #apple
                pygame.draw.rect(window, appleColor, (j*segmentWidth, i*segmentHeight, segmentWidth, segmentHeight))
    
    pygame.display.update()


def keyboardInput():
    global direction
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and not direction[0] == 1:
        direction = (-1, 0)

    if keys[pygame.K_RIGHT] and not direction[0] == -1:
        direction = (1, 0)

    if keys[pygame.K_UP] and not direction[1] == 1:
        direction = (0, -1)

    if keys[pygame.K_DOWN] and not direction[1] == -1:
        direction = (0, 1)

def moveSnake():
    global direction, snakeBody, map, alive, mapWidth, mapHeight, apple
    head = snakeBody[0]
    newHead = (head[0] + direction[0], head[1] + direction[1])
     
    if newHead[0] <= -1:
        newHead = (mapWidth-1, newHead[1])

    if newHead[0] >= mapWidth:
        newHead = (0, newHead[1])

    if newHead[1] <= -1:
        newHead = (newHead[0], mapHeight-1)

    if newHead[1] >= mapHeight:
        newHead = (newHead[0], 0)

    map[snakeBody[len(snakeBody) - 1][1]][snakeBody[len(snakeBody)-1][0]] = 0

    snakeBody.insert(0, newHead)
    if not newHead == apple:
        snakeBody.pop()

    else:
        apple = spawnApple()

    for i in range(0, len(snakeBody)-1):
        if snakeBody[i] == newHead and not i == 0:
            alive = False
        
        else:
            map[snakeBody[i][1]][snakeBody[i][0]] = 1

while(alive):
    pygame.time.delay((int)(1000 * speed))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            alive = False
    
    keyboardInput()
    moveSnake()
    updateMap()

pygame.quit()
