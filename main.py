#------------------------------------------------------------------#
#  EZnake v0.95c                                                #
#   Christoffer 'Auradiamus' Hansen                                #
#    main.py                                                       #
#------------------------------------------------------------------#

###imports###
import pygame
import random

###globals###
##Resolution##
#Canvas#
res = (800,600) #Resolution of the window
##Colours & images##
RGBWhite = (255,255,255) #RGB code for white
RGBBlack = (0,0,0) #RGB code for black
RGBSnakeGreen = (12,185,0) #RGB code for darker green
RGBAppleRed = (228,3,3) #RGB code for slighty darker red
imgSnakeHead = pygame.image.load('resources/snakeHead.png')
imgAppleRed = pygame.image.load('resources/appleRed.png')
##Speeds##
minSpeed = 10 #Minimum speed / starting speed of the snake
maxSpeed = 40 #Maximum speed of the snake
currentSpeed = minSpeed #Current speed of the snake
##System##
fps = 20 #FPS the game is to run in
font = '' #Default font variable just to make it global
gameDisplay = pygame.display.set_mode(res) #The canvas of the game
##Game values##
score = 0
snakeSize_Score = 0
blockSize = 10
appleThickness = 10
gameOver = False
gameExit = False
randRedAppleX = 0.0
randRedAppleY = 0.0
snakeLength = 1

###functions###
def _getVersion():
    return '0.95c'

def _update(): #Updates display
    pygame.display.update()

def _init(title): #Init game with %s as parameter
    global font, fontScreen, gameDisplay #Calls global vars so you can change them
    pygame.init() #Inits the game *REQUIREMENT*
    pygame.display.set_caption(title) #Sets the title of the window
    font = pygame.font.SysFont(None, 24, False, False) #Font to use. Default*
    _update() #Updates gameDisplay

def _messageToScreen(msg, colour):
    global gameDisplay
    displayText = font.render(msg, True, colour)
    gameDisplay.blit(displayText, [res[0]/4, res[1]/2])

def _snake(b, snakeList):
    for XnY in snakeList:
        #print('[DEBUG] Snake head at [%d,%d]' % (head_x, head_y))
        pygame.draw.rect(gameDisplay, RGBSnakeGreen, [XnY[0],XnY[1], b, b]) #Creates the snake


def _gameLoop(): #Game loop
    global currentSpeed, gameExit, gameOver, randRedAppleX, randRedAppleY, snakeLength

    snakeLength = 1
    snakeList = []

    head_x = res[0]/2 #Starting pos x (resoluton divided by 2)
    head_y = res[1]/2 #Starting pos y (resoluton divided by 2)
    head_x_change = 0
    head_y_change = 0

    randRedAppleX = random.randrange(10, res[0]-blockSize, blockSize)
    randRedAppleY = random.randrange(10, res[1]-blockSize, blockSize)

    clock = pygame.time.Clock()

    while not gameExit:
        while gameOver == True: #if GameOver is equal to True
            gameDisplay.fill(RGBWhite) #Fill whole screen white
            _messageToScreen('Game over, Press C to try again or X to exit the game.', RGBAppleRed) #Send msg to screen in red
            _update() #Update display
            for event in pygame.event.get(): #Calls eventHandler
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN: #If a key is pressed
                    if event.key == pygame.K_c: #If key is c
                        gameExit = False
                        gameOver = False
                        _gameLoop()
                    if event.key == pygame.K_x: #If key is x
                        gameExit = True
                        gameOver = False

        for event in pygame.event.get(): #Calls eventHandler
            if event.type == pygame.QUIT:
                print('[ACTION] QUIT has been called.')
                gameExit = True
                gameOver = False
            elif event.type == pygame.KEYDOWN: #If a key is pressed
                if event.key == pygame.K_UP: #If key is UP
                    print('[ACTION] K_UP')
                    head_y_change = -currentSpeed
                    head_x_change = 0
                elif event.key == pygame.K_DOWN: #If key is DOWN
                    print('[ACTION] K_DOWN')
                    head_y_change = currentSpeed
                    head_x_change = 0
                elif event.key == pygame.K_LEFT: #If key is LEFT
                    print('[ACTION] K_LEFT')
                    head_x_change = -currentSpeed
                    head_y_change = 0
                elif event.key == pygame.K_RIGHT: #If key is RIGHT
                    print('[ACTION] K_RIGHT')
                    head_x_change = currentSpeed
                    head_y_change = 0
                elif event.key == pygame.K_x: #If key is x
                    print('[ACTION] K_x')
                    gameExit = True
                    gameOver = False

        #Checks position of the snake, to see if it has hit the boundary or an apple
        _checkPos(head_x, head_y)

        head_x += head_x_change
        head_y += head_y_change

        gameDisplay.fill(RGBBlack)
        #print('[DEBUG] appleRed created at [%d,%d]' % (randRedAppleX, randRedAppleY))
        pygame.draw.rect(gameDisplay, RGBAppleRed, [randRedAppleX, randRedAppleY, appleThickness, appleThickness])

        snakeHead = []
        snakeHead.append(head_x)
        snakeHead.append(head_y)
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:
            del snakeList[0]

        for e in snakeList[:-1]:
            if e == snakeHead:
                gameOver = True

        _snake(blockSize, snakeList)
        _update() #Updates display

        clock.tick(fps)

def _checkPos(head_x, head_y):
    global gameOver, randRedAppleX, randRedAppleY, score, snakeLength
    #If snake enters boundaries: End game.
    if head_x >= res[0] or head_x <= 0 or head_y >= res[1] or head_y <= 0:
        print('[EVENT] Snake entered boundary at [%d,%d]' % (head_x, head_y))
        gameOver = True

    #If Snake head crosses the X or Y of the red apple
    if head_x >= randRedAppleX and head_x <= randRedAppleX+appleThickness-blockSize:
        if head_y >= randRedAppleY and head_y <= randRedAppleY+appleThickness-blockSize:
            score += 10 #Increment score by 10
            snakeLength += 2 #Increment snake length by 2
            randRedAppleX = random.randrange(10, res[0]-blockSize, blockSize) #new X for new red apple
            randRedAppleY = random.randrange(10, res[1]-blockSize, blockSize) #new Y for new red apple

###main###
_init('EZnake v')
_gameLoop()
pygame.quit()
quit()
