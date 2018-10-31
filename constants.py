import pygame as p

#RGB Codes
RGBWhite = (255,255,255)
RGBBlack = (0,0,0)
RGBSnakeGreen = (12,185,0)
RGBAppleRed = (228,3,3)
#Images
icon = p.display.set_icon(p.image.load(r'resources\art\Znake-icon.png'))
imgSnakeHead = p.image.load(r'resources\art\snakeHead.png')
imgAppleRed = p.image.load(r'resources\art\redApple.png')
#Sound#
ateFood = r'resources\sound\ateFood.ogg'
bgMusic = r'resources\sound\bgMusic.mp3'
crash = r'resources\sound\crash.ogg'
#Game values#
blockSize = 10
appleThickness = 10
minSpeed = 10
#System#
resolution = (400,400)
fps = 20
