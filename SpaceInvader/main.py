import pygame
import random
import math
from pygame import mixer, mixer_music
# Initializing pygame
pygame.init()

# Background
background = pygame.image.load('./images/game-bg.jpg')

#background music
mixer.music.load('./Sounds/bg-music.wav')
mixer.music.play(-1)

# Creating Screen
screen = pygame.display.set_mode((800, 600))

# Title and icon
pygame.display.set_caption('Space Invader')
icon = pygame.image.load('./images/ufo.png')
pygame.display.set_icon(icon)

# player spaceship
player = pygame.image.load('./images/space-ship.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# scoring system
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
scoreBoardX = 15
scoreBoardY = 15
def scoreBoard(x, y):
    renderedScore = font.render('Score:' + ' ' + str(score), True, (129, 216, 208))
    screen.blit(renderedScore, (x, y))

#Game over screen
gameOverText = pygame.font.Font('freesansbold.ttf', 65)

def gameOver():
    over = font.render('GAME OVER', True, (129, 216, 208))
    screen.blit(over, (300, 300))

# Alien
alien = []
alienX = []
alienY = []
alienX_change = []
alienY_change = []

aliens = 6
for i in range(aliens):
    alien.append(pygame.image.load('./images/alien.png'))
    alienX.append(random.randint(0, 736))
    alienY.append(random.randint(50, 150))
    alienX_change.append(0.2)
    alienY_change.append(30)

# Bullet
bullet = pygame.image.load('./images/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
# cant see bullet on screen
bullet_status = 'ready'

def playerFung(x, y):
    screen.blit(player, (x, y))

def alienFung(x, y, i):
    screen.blit(alien[i], (x, y))

def bulletFung(x, y):
    global bullet_status
    bullet_status = 'fire'
    screen.blit(bullet, (x + 18, y))

def collision(alienX, alienY, playerX, playerY):
    distance = math.sqrt((math.pow((alienX - bulletX), 2)) + (math.pow((alienY - bulletY), 2)))
    if distance < 30:
        return True
    else:
        return False

# opening and closing game screen
data = True
while data:
    # background-img
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            data = False

        # check if right or left keystroke
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.4
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.4

            if event.key == pygame.K_SPACE:
                if bullet_status is 'ready':
                    #bullet sound
                    bullet_sound = mixer.Sound('./Sounds/laser.wav')
                    bullet_sound.play()
                    #assign coordinate X of space-ship to bullets x coordinate
                    bulletX = playerX
                    bulletFung(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # to make spaceship move
    playerX += playerX_change

    # to keep spaceship on screen
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536

    # to make alien move
    for i in range(aliens):
        if alienY[i] > 400:
            for j in range(aliens):
                alienY[j] = 2000

            #game over
            gameOver()
            break
        alienX[i] += alienX_change[i]
        # alienY += alienY_change

        # to keep alien on screen
        if alienX[i] <= 0:
            alienX_change[i] = 0.2
            alienY[i] += alienY_change[i]
        elif alienX[i] >= 736:
            alienX_change[i] = -0.2
            alienY[i] += alienY_change[i]

        # Shooting Alien
        shoot = collision(alienX[i], alienY[i], bulletX, bulletY)
        if shoot:
            shoot_collide = mixer.Sound('./Sounds/boom.wav')
            shoot_collide.play()
            bulletY = 480
            bullet_status = 'ready'
            score += 1
            # print(score)
            alienX[i] = random.randint(0, 736)
            alienY[i] = random.randint(50, 150)
        alienFung(alienX[i], alienY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_status = 'ready'
    if bullet_status is 'fire':
        bulletFung(bulletX, bulletY)
        bulletY -= bulletY_change

    playerFung(playerX, playerY)
    scoreBoard(scoreBoardX, scoreBoardY)
    pygame.display.update()

pygame.quit()
