import pygame
from random import randint
from math import sqrt, pow
from settings import *

# Initializing the game
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Setting the Title for the Game
pygame.display.set_caption("Space Invadors")

# Setting the Icon For the Game
icon = pygame.image.load('images/logo.png')
pygame.display.set_icon(icon)

# Background Image
backgroundImage = pygame.image.load('images/background.png')

# Adding the Player to the Game
playerSpaceShip = pygame.image.load('images/spaceShip.png')
playerXCoordinate = 380
playerYCoordinate = 500
playerPositionChange = 0

# Drawing player into the Screen
def player(spaceship_xcoor, spaceship_ycoor):
    screen.blit(playerSpaceShip, (spaceship_xcoor, spaceship_ycoor))

# Enemy Settings
enemySpaceShip = list()
enemyXCoordinate = list()
enemyYCoordinate = list()
enemyX_position_change = list()
enemyY_position_change = list()
enemiesCount = 7

for i in range(enemiesCount):
    enemySpaceShip.append(pygame.image.load('images/enemy.png'))
    enemyXCoordinate.append(randint(0, 735))
    enemyYCoordinate.append(randint(25, 150))
    enemyX_position_change.append(4.5)
    enemyY_position_change.append(35)

def enemy(enemy_xcoor, enemy_ycoor, index):
    screen.blit(enemySpaceShip[index], (enemy_xcoor, enemy_ycoor))

# Bullet Settings
bulletImage = pygame.image.load('images/bullet.png')
bulletXCoordinate = 0
bulletYCoordinate = 500
bulletY_position_change = 7
# Initially Setting the Bullet to ready state.
bulletState = "ready" 

def fireBullet(bullet_xcoor, bullet_ycoor):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImage, (bullet_xcoor + 16, bullet_ycoor + 10))

# Collision Detection
def isCollide(enemy_xcoor, enemy_ycoor, bullet_xcoor, bullet_ycoor):
    collisionValue = sqrt(pow(enemy_xcoor - bullet_xcoor, 2) + pow(enemy_ycoor - bullet_ycoor, 2))
    if(collisionValue < 27):
        return True
    else:
        return False

# Setting the Score Card for the Game
font = pygame.font.Font('fonts/font.ttf', 25)
score_xcoor = 10
score_ycoor = 10

def displayScore(scoreX, scoreY):
    score = font.render("Score :{}".format(SCORE), True, (255, 255, 255))
    screen.blit(score, (scoreX, scoreY))


running = True

while running:

    # Setting the Color for the Game Board
    screen.fill((133, 85, 79))

    # Setting the background image
    screen.blit(backgroundImage, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerPositionChange = -4.0           
            if event.key == pygame.K_RIGHT:
                playerPositionChange = 4.0
            if event.key == pygame.K_SPACE:
                if bulletState is "ready":
                    bulletXCoordinate = playerXCoordinate
                    fireBullet(bulletXCoordinate, bulletYCoordinate)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerPositionChange = 0
        

    # Calling the Player Function to Draw the Spaceship into the Screen
    # Chainging the Player Position
    playerXCoordinate += playerPositionChange
    
    # Setting the Boundaries for the Spaceship
    if(playerXCoordinate <= 0):
        playerXCoordinate = 0
    elif(playerXCoordinate >= 736):
        playerXCoordinate = SCREEN_WIDTH - 64

    for i in range(enemiesCount):

        # Enemy Movemnt Strategy
        enemyXCoordinate[i] += enemyX_position_change[i]

        # Setting Boundaries for Enemies and Handling the Corner Cases
        if(enemyXCoordinate[i] <= 0):
            enemyXCoordinate[i] = 0
            enemyX_position_change[i] = 4.5
            enemyYCoordinate[i] += enemyY_position_change[i]
        elif(enemyXCoordinate[i] >= 736):
            enemyXCoordinate[i] = 736
            enemyX_position_change[i] = -4.5
            enemyYCoordinate[i] += enemyY_position_change[i]

        collision = isCollide(enemyXCoordinate[i], enemyYCoordinate[i], bulletXCoordinate, bulletYCoordinate)

        if(collision):
            bulletState = 'ready'
            bulletYCoordinate = 500
            SCORE += 1
            enemyXCoordinate[i] = randint(0, 735)
            enemyYCoordinate[i] = randint(25, 150)
        
        enemy(enemyXCoordinate[i], enemyYCoordinate[i], i)
   
    # screen.blit(bulletImage, (playerXCoordinate + 25, 350))
    # Bullet Movement
    if(bulletState is 'fire'):
        fireBullet(bulletXCoordinate, bulletYCoordinate)
        bulletYCoordinate -= bulletY_position_change
        if(bulletYCoordinate <= 0):
            bulletYCoordinate = 500
            bulletState = 'ready'
    

    player(playerXCoordinate, playerYCoordinate)

    # Updating the Game Window with Score
    displayScore(score_xcoor, score_ycoor)
    # Overall Update
    pygame.display.update()