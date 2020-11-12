import pygame
import random
import math
from pygame import mixer

# init initiates the game
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('background.png')

# Music
mixer.music.load('background.wav')
mixer.music.play(-1)

# Set Display
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('space-ship.png')
playerX = 370
playerY = 480
playerX_change = 0.1

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies = 6

for i in range(num_enemies):
    enemyImg.append(pygame.image.load('alien ship.png'))
    enemyX.append(random.randint(0, 600))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(20)

# bullet
bulletImg = pygame.image.load('bullets_fire.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 40
bullet_state = "ready"
score = 0

# add the font for score
font = pygame.font.Font('SuperMario256.ttf', 32)
font2 = pygame.font.Font('baby blocks.ttf', 32)
textX = 20
textY = 20


def show_score(x, y):
    score_value = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_value, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fireBullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    bullet_sound = mixer.Sound('laser.wav')
    bullet_sound.play()
    screen.blit(bulletImg, (x + 16, y + 10))


# collision
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 24:
        explosion_sound = mixer.Sound('explosion.wav')
        explosion_sound.play()
        return True
    return False
#Game Over
def game_over_text():
    over_text = font.render("GAME OVER \n Score: " + str(score), True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

# Game Loop

running = True

while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                # print('Right Arrow is pressed')
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                # print('Right Arrow is pressed')
                bulletX = playerX
                fireBullet(playerX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0
                # print("Keystroke has been released")

    playerX += playerX_change
    if playerX < 0:
        playerX = 0
    if playerX > 735:
        playerX = 735

    for i in range(num_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyY[i]> 450:
            for j in range(num_enemies):
                enemyY[i] = 2000
            game_over_text()
            break
        if enemyX[i] < 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        if enemyX[i] > 735:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score += 1
            enemyX[i] = random.randint(0, 600)
            enemyY[i] = random.randint(50, 150)
            print(score)

        enemy(enemyX[i], enemyY[i], i)
    # bullet movement
    if bullet_state == "fire":

        fireBullet(bulletX, bulletY)
        bulletY -= bulletY_change
        if bulletY <= 0:
            bulletY = 480
            bullet_state = 'ready'

    show_score(textX, textY)
    player(playerX, playerY)

    pygame.display.update()
