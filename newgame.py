import pygame
import random
from pygame.locals import *

pygame.init()
win = pygame.display.set_mode((400, 600))
font = pygame.font.SysFont("comicsans", 20, True)

pygame.display.set_caption("simple game")

bg = pygame.image.load("bg2.png")
fly = pygame.image.load("air2.png")
ene = pygame.image.load("air3.png")
clock = pygame.time.Clock

count = z = 0
a = 0
score = 0
i = 0
n = 0



class player():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 4
        self.count = 0
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.health = 100
        self.damage = 5
        self.damageout = 5

    def draw(self, win):
        win.blit(fly, (self.x, self.y))
        self.hitbox = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
        pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 7, 40, 5))
        pygame.draw.rect(win, (0, 100, 0), (self.hitbox[0], self.hitbox[1] - 7, self.health//2.5, 5))

    def hitme(self):
        print("ohh")


class enemy(object):
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.vel = 2
        self.r = 200
        self.r1 = 148
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.health = 10
        self.visible = True

    def draw(self, win):
        self.move()
        if self.visible:
            win.blit(ene, (self.x, self.y))
            self.hitbox = (self.x, self.y, self.width, self.height)
            pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 7, 40, 5))
            pygame.draw.rect(win, (0, 100, 0), (self.hitbox[0], self.hitbox[1] - 7, 40 - (4 * (10 - self.health)), 5))

    def hit(self):
        print("hit")

    def move(self):
        if self.r == self.x:
            self.r = random.randrange(6, 352, self.vel)
        if self.r >= self.x:
            self.x += self.vel
        else:
            self.x -= self.vel
        if self.r1 == self.y:
            self.r1 = random.randrange(30, 162, self.vel)
        if self.r1 >= self.y:
            self.y += self.vel
        else:
            self.y -= self.vel
        if self.health <= 0:
            enemyspot.pop(enemyspot.index(self))


def drawWindow():
    global score
    global z
    global i
    rel_z = z % bg.get_rect().height
    win.blit(bg, (0, rel_z - bg.get_rect().height))
    if rel_z < 600:
        win.blit(bg, (0, rel_z))
    z += 2
    plane.draw(win)
    for enem in enemyspot:
        enem.draw(win)
    text = font.render("Score: " + str(int(score)), 1, (255, 255, 255))
    win.blit(text, (315, 5))
    pygame.display.update()


plane = player(180, 450, 38, 38)
enemyspot = []





run = True
while run:
    clock().tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
    if len(enemyspot) < 5:
        r3 = random.randrange(100, 200, 20)
        enemyspot.append(enemy(r3, -200, 40, 40, 450))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and plane.x > 5:
        plane.x -= plane.vel
        right = False
        left = True
    elif keys[pygame.K_RIGHT] and plane.x < 355:
        plane.x += plane.vel
        right = True
        left = False
    else:
        right = False
        left = False
    if keys[pygame.K_UP] and plane.y > 300:
        plane.y -= plane.vel
    if keys[pygame.K_DOWN] and plane.y < 525:
        plane.y += plane.vel
    score += 1
    drawWindow()