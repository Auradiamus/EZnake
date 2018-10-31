#------------------------------------------------------------------#
#  EZnake v0.95c                                                #
#   Christoffer 'Auradiamus' Hansen                                #
#    main.py                                                       #
#------------------------------------------------------------------#

###imports###
import pygame
import random
import constants as c

###Globals###
font = '' #Default font variable just to make it global
gameDisplay = pygame.display.set_mode(c.resolution) #The canvas of the game
cSpeed = c.minSpeed #Current speed of the snake
score = 0
gameOver = False
gameExit = False
randRedAppleX = 0.0
randRedAppleY = 0.0
snakeLength = 1
direction = 'UP'

###functions###
def _getVersion():
    return '1.00'

def _intro():
    tmp = True
    while tmp:
        gameDisplay.fill(c.RGBWhite)
        gameDisplay.blit(c.imgAppleRed, [(c.resolution[0]/2)-40, (c.resolution[1]/2)-107])
        _msgToScreen(' Znake ', c.RGBBlack, 30, -100)
        gameDisplay.blit(c.imgAppleRed, [(c.resolution[0]/2)+30, (c.resolution[1]/2)-107])
        _msgToScreen('By Auradiamus', c.RGBBlack, 14, -80)
        _msgToScreen('Press C to start!', c.RGBAppleRed, 24, 0)
        _msgToScreen('Press X to quit!', c.RGBAppleRed, 24, 20)
        _msgToScreen('Press P to pause!', c.RGBAppleRed, 24, 40)

        _update()

        for event in pygame.event.get(): #Calls eventHandler
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN: #If a key is pressed
                if event.key == pygame.K_c: #If key is c
                    tmp = False
                elif event.key == pygame.K_x:
                    pygame.quit()
                    quit()

def _update(): #Updates display
    pygame.display.update()

def _init(title): #Init game with %s as parameter
    global fontScreen, gameDisplay #Calls global vars so you can change them
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init() #Inits the game *REQUIREMENT*
    pygame.display.set_caption(title) #Sets the title of the window
    c.icon
    _update() #Updates gameDisplay

def _tObjects(msg, colour):
    tSurface = font.render(msg, True, colour)
    return tSurface, tSurface.get_rect()

def _msgToScreen(msg, colour, size, y):
    global font
    font = pygame.font.SysFont(None, size, False, False) #Font to use. Default*
    tSurface, tRectangle = _tObjects(msg, colour)
    tRectangle.center = (c.resolution[0]/2), (c.resolution[1]/2)+y
    gameDisplay.blit(tSurface, tRectangle)

def _genApple():
    global randRedAppleX, randRedAppleY
    randRedAppleX = random.randrange(10, c.resolution[0]-c.blockSize, c.blockSize)
    randRedAppleY = random.randrange(10, c.resolution[1]-c.blockSize, c.blockSize)

def _snake(b, snakeList):

    #Rotating the snake head depending on the direction
    if direction == 'UP':
        head = c.imgSnakeHead
    elif direction == 'RIGHT':
        head = pygame.transform.rotate(c.imgSnakeHead, 270)
    elif direction == 'DOWN':
        head = pygame.transform.rotate(c.imgSnakeHead, 180)
    elif direction == 'LEFT':
        head = pygame.transform.rotate(c.imgSnakeHead, 90)

    gameDisplay.blit(head, (snakeList[-1][0], snakeList[-1][1]))

    for XnY in snakeList[:-1]:
        pygame.draw.rect(gameDisplay, c.RGBSnakeGreen, [XnY[0],XnY[1], b, b]) #Creates the body of the snake

def _pause():
    paused = True

    #gameDisplay.fill(c.RGBWhite)
    _msgToScreen('Paused!', c.RGBAppleRed, 50, -100)
    _msgToScreen('Press C to unpause!', c.RGBWhite, 24, 0)
    _msgToScreen('Press X to quit!', c.RGBWhite, 24, 20)

    while paused:
        #Eventhandler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_x:
                    pygame.quit()
                    quit()
        _update()

def _scoreToScreen():
    tScore = font.render('Score: '+str(score), True, c.RGBAppleRed)
    gameDisplay.blit(tScore, [0,0])

def _gameLoop(): #Game loop
    global gameExit, gameOver, snakeLength, score, direction

    bgMusic = pygame.mixer.music.load(c.bgMusic)
    pygame.mixer.music.play(-1)

    score = 0
    direction = 'UP'
    snakeLength = 3
    snakeList = []

    head_x = c.resolution[0]/2 #Starting pos x
    head_y = c.resolution[1]/2 #Starting pos y
    head_x_change = 0
    head_y_change = -10 #Starts the snake moving at the direction 'UP' (@tNorth)

    _genApple()

    clock = pygame.time.Clock()

    while not gameExit:
        while gameOver == True: #if GameOver is equal to True
            gameDisplay.fill(c.RGBWhite) #Fill whole screen white
            _msgToScreen('Game over!', c.RGBAppleRed, 24, -30) #Send msg to screen in red
            _msgToScreen(('Score: '+str(score)), c.RGBBlack, 24, 0)
            _msgToScreen('Press C to try again or X to exit the game.', c.RGBBlack, 24, 30)
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
                    elif event.key == pygame.K_x: #If key is x
                        pygame.quit()
                        quit()

        for event in pygame.event.get(): #Calls eventHandler
            if event.type == pygame.QUIT:
                print('[ACTION] QUIT has been called.')
                gameExit = True
                gameOver = False
            elif event.type == pygame.KEYDOWN: #If a key is pressed
                if event.key == pygame.K_UP: #If key is UP
                    if direction != 'DOWN' and direction != 'UP':
                        print('[ACTION] K_UP')
                        direction = 'UP'
                        head_y_change = -cSpeed
                        head_x_change = 0
                elif event.key == pygame.K_DOWN: #If key is DOWN
                    if direction != 'UP' and direction != 'DOWN':
                        print('[ACTION] K_DOWN')
                        direction = 'DOWN'
                        head_y_change = cSpeed
                        head_x_change = 0
                elif event.key == pygame.K_LEFT: #If key is LEFT
                    if direction != 'RIGHT' and direction != 'LEFT':
                        print('[ACTION] K_LEFT')
                        direction = 'LEFT'
                        head_x_change = -cSpeed
                        head_y_change = 0
                elif event.key == pygame.K_RIGHT: #If key is RIGHT
                    if direction != 'LEFT' and direction != 'RIGHT':
                        print('[ACTION] K_RIGHT')
                        direction = 'RIGHT'
                        head_x_change = cSpeed
                        head_y_change = 0
                elif event.key == pygame.K_p:
                    _pause()

        #Checks position of the snake, to see if it has hit the boundary or an apple
        _checkPos(head_x, head_y)

        head_x += head_x_change
        head_y += head_y_change

        gameDisplay.fill(c.RGBBlack) #Fills the canvas with the colour c.RGBBlack
        gameDisplay.blit(c.imgAppleRed, [randRedAppleX, randRedAppleY]) #Creates an apple on the canvas

        #Snake body
        snakeHead = []
        snakeHead.append(head_x)
        snakeHead.append(head_y)
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:
            del snakeList[0]

        for e in snakeList[:-1]:
            if e == snakeHead:
                crash = pygame.mixer.Sound(c.crash)
                crash.play()
                gameOver = True

        _snake(c.blockSize, snakeList)
        _scoreToScreen()
        _update() #Updates display

        clock.tick(c.fps)

def _checkPos(head_x, head_y):
    global gameOver, score, snakeLength
    #If snake enters boundaries: End game.
    if head_x > c.resolution[0] or head_x < 0 or head_y > c.resolution[1] or head_y < 0:
        crash = pygame.mixer.Sound(c.crash)
        crash.play()
        gameOver = True

    #If Snake head crosses the X or Y of the red apple
    if head_x >= randRedAppleX and head_x <= randRedAppleX+c.appleThickness-c.blockSize:
        if head_y >= randRedAppleY and head_y <= randRedAppleY+c.appleThickness-c.blockSize:
            ateFood = pygame.mixer.Sound(c.ateFood)
            ateFood.play()
            score += 10 #Increment score by 10
            snakeLength += 2 #Increment snake length by 2
            _genApple()

###main###
_init('EZnake')
_intro()
_gameLoop()
pygame.quit()
quit()
