import pygame
import random
import math
from pygame import mixer

pygame.init()

clock = pygame.time.Clock()
# screen
screen = pygame.display.set_mode((800, 600))

# background music
music = pygame.mixer.Sound('music1.mp3')


# tree
tree = pygame.image.load('treePineSnowRound.png')
treeX = 100
treeY = 345

# cloud
cloud = pygame.image.load('background_cloudA.png')
cloud = pygame.transform.scale(cloud, (128, 40))
cloudX = 200
cloudY = 35

# cloud 2

cloudA = pygame.image.load('background_cloudA.png')
cloud = pygame.transform.scale(cloud, (128, 40))
cloudAX = 570
cloudAY = 35

# background
background = pygame.image.load('background.png')
# ground
ground = pygame.image.load('groundSnow.png')

# game name and icon
pygame.display.set_caption("Clifer")
icon = pygame.image.load('snowman.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('character_roundRed.png')
playerImg = pygame.transform.scale(playerImg, (64, 64))
playerX = 400
playerY = 420
playerX_Change = 0

# coin
coin = pygame.image.load('coin.png')
coin = pygame.transform.scale(coin, (32,32))
coinX = random.randint(75, 750)
coinY = 300

# snow enemy
snowImg =[]
snowX =[]
snowY = []
#snowY_change =[]

num_of_snow = 5

snowY_change = 2.1

for i in range(num_of_snow):
    snowImg.append(pygame.transform.scale(pygame.image.load('tile_bush.png'), (32, 32)))
    snowX.append(random.randint(0, 790))
    snowY.append(random.randint(5, 55))
    #snowY_change.append(2.1)

# arrow
arrowImg = pygame.image.load('item_arrow.png')
arrowX = -200
arrowY = 430
X_change = 3.5


# jumping
jumping = False
Y_Gravity = 1
jump_Height = 18
Y_Velociy = jump_Height

# life
hit = 0
heartImg = pygame.image.load('heart.png')
heartImg = pygame.transform.scale(heartImg, (23, 23))

# score
score_value= 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

#game over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (0, 0, 0))
    screen.blit(over_text, (200, 250))

def show_score(x,y):
    score = font.render("Score :" + str(score_value), True, (0, 0, 0))
    screen.blit(score,(x, y))


def lifefun(x,y):
    screen.blit(heartImg, (x, y))

def cloudfun(x,y):
    screen.blit(cloud, (x, y))

def treefun(x,y):
    screen.blit(tree, (x, y))
def coinfun(x,y):
    screen.blit(coin, (x,y))

def player(x,y) :
    screen.blit(playerImg, (x, y))

def snow(x,y,z):
    screen.blit(snowImg[z], (x, y))

def arrow(x, y):
    screen.blit(arrowImg, (x, y))

def isCollide(arrowX,arrowY,playerX,playerY):
    distance = math.sqrt((math.pow((arrowX-playerX), 2)) + (math.pow((arrowY-playerY), 2)))
    if distance <= 32:
        return True
    else:
        return False



running = True

while running:

    screen.fill((116, 86, 68))

    # background
    screen.blit(background, (0,0))

    # cloud
    cloudfun(cloudX,cloudY)

    #cloud
    cloudfun(cloudAX,cloudAY)
    # tree
    treefun(treeX, treeY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # keystoke
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_Change = -2
            if event.key == pygame.K_RIGHT:
                playerX_Change = 2
            if event.key == pygame.K_UP:
                if hit>= 4:
                    jumping = False
                else:
                    jumping = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_Change = 0

    if jumping:
        playerY -= Y_Velociy
        Y_Velociy -= Y_Gravity
        if Y_Velociy < - jump_Height:
            jumping = False
            Y_Velociy = jump_Height


    playerX += playerX_Change

    # don't go outside
    if playerX <= -5:
        playerX =-5
    elif playerX >= 743:
        playerX = 743

    player(playerX, playerY)

    #repeat arrow
    arrowX += X_change
    if arrowX >=1200:
        arrowX = -200
    arrow(arrowX,arrowY)

    # collide of arrow
    if isCollide(arrowX,arrowY,playerX,playerY):
        arrowX = -400
        hit += 1
        print(hit)

    # collide of snow
    for i in range(num_of_snow):
        # game over
        if hit >= 4:
            playerImg = pygame.image.load('character_roundPurple_over.png')
            playerImg = pygame.transform.scale(playerImg, (64, 64))
            for j in range(num_of_snow):
                snowY[j] = 5000
            arrowX = 5000

            game_over_text()

            break



        if isCollide(snowX[i], snowY[i], playerX, playerY):
            snowY[i] = random.randint(5, 55)
            hit += 1

        snowY[i] += snowY_change
        snow(snowX[i], snowY[i], i)
        if snowY[i] >= 449:
            snowX[i] = random.randint(0, 790)
            snowY[i] = random.randint(5, 55)
    # character color change
    if hit == 1:
        playerImg = pygame.image.load('character_roundGreen.png')
        playerImg = pygame.transform.scale(playerImg, (64, 64))

    elif hit == 2:
        playerImg = pygame.image.load('character_roundYellow.png')
        playerImg = pygame.transform.scale(playerImg, (64, 64))
    elif hit == 3:
        playerImg = pygame.image.load('character_roundPurple.png')
        playerImg = pygame.transform.scale(playerImg, (64, 64))

    # coin
    coinfun(coinX, coinY)
    if isCollide(coinX,coinY,playerX,playerY):
        score_value += 1
        coinX = random.randint(75, 750)

    show_score(textX, textY)

    # speed up
    speed_check = score_value+1
    is_Divide = speed_check % 4
    if is_Divide == 0:
        speed_check = score_value +2
        snowY_change += .00001

    #show life
    if hit == 0:
        lifefun(600, 20)
        lifefun(650, 20)
        lifefun(700, 20)
        lifefun(750, 20)

    if hit == 1:
        lifefun(650, 20)
        lifefun(700, 20)
        lifefun(750, 20)

    if hit == 2:
        lifefun(700, 20)
        lifefun(750, 20)

    if hit == 3:
        lifefun(750, 20)

    #music
    music.play()

    pygame.display.update()
    clock.tick(60)