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
blow = [pygame.image.load("blow1.png"), pygame.image.load("blow2.png"), pygame.image.load("blow3.png"),
        pygame.image.load("blow4.png"), pygame.image.load("blow5.png"), pygame.image.load("blow6.png")]
clock = pygame.time.Clock

count = z = 0
a = 0
score, kill = 0, 0
right = False
left = False
i = 0
n = 0


class shoot():
    def __init__(self, x, y, radius, color, vel):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel = vel

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


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
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
        self.count += 1
        if self.count % 20 == 0:
            bullets1.append(
                shoot((round(self.x + self.width // 2)), round((self.y + self.height // 2) - 25), 3,
                      (0, 255, 0), 20))
            self.count = 0
        win.blit(fly, (self.x, self.y))
        pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 7, 40, 5))
        pygame.draw.rect(win, (0, 100, 0), (self.hitbox[0], self.hitbox[1] - 7, self.health // 2.5, 5))

    def hitme(self):
        print("ohh")
        if self.health > 5:
            self.health -= self.damage
        else:
            pass
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
        self.count = 0
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.health = 10
        self.visible = True

    def draw(self, win):
        self.move()
        if self.visible:
            win.blit(ene, (self.x, self.y))
            self.hitbox = (self.x, self.y, self.width, self.height)
            # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 7, 40, 5))
            pygame.draw.rect(win, (0, 100, 0), (self.hitbox[0], self.hitbox[1] - 7, 40 - (4 * (10 - self.health)), 5))
            self.count += 1
            if self.count % 60 == 0:
                bullets2.append(
                    shoot((round(self.x + self.width // 2)), round((self.y + self.height // 2) + 25), 3,
                          (255, 0, 0), -5))
                self.count = 0

    def hit(self):
        if plane.damageout <= self.health:
            self.health -= plane.damageout
        else:
            self.health -= self.health

    def move(self):
        global kill
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
            kill += 1
            blows.append(bloww(self.x, self.y))
            enemyspot.pop(enemyspot.index(self))


class bloww():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, win):
        self.move()
        win.blit(blow[(i // 4)], (self.x, self.y))

    def move(self):
        self.y += 3


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
    for blo in blows:
        blo.draw(win)
        i += 1
        if i == 24:
            blows.pop(blows.index((blo)))
            i = 0
    for enem in enemyspot:
        enem.draw(win)
    for bullet in bullets1:
        bullet.draw(win)
    for bullet in bullets2:
        bullet.draw(win)
    text = font.render("Score: " + str(int(score)), 1, (255, 255, 255))
    win.blit(text, (315, 5))
    text1 = font.render("Kills: " + str(int(kill)), 1, (255, 255, 255))
    win.blit(text1, (5, 5))
    pygame.display.update()


plane = player(180, 450, 38, 38)
enemyspot = []
bullets1 = []
bullets2 = []
blows = []

run = True
while run:
    clock().tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
    if len(enemyspot) < 5:
        r3 = random.randrange(100, 200, 20)
        enemyspot.append(enemy(r3, -200, 40, 40, 450))
    for bullet in bullets2:
        if bullet.y < 600 and bullet.y > 0:
            bullet.y -= bullet.vel
        elif len(bullets2) > 1:
            bullets2.pop(bullets2.index(bullet))
        if bullet.x + bullet.radius > plane.hitbox[0] and bullet.x - bullet.radius < plane.hitbox[0] + plane.hitbox[
            2]:
            if bullet.y - bullet.radius < plane.hitbox[1] + plane.hitbox[3] and bullet.y + bullet.radius > \
                    plane.hitbox[1]:
                plane.hitme()
                bullets2.pop(bullets2.index(bullet))
    for bullet in bullets1:
        if bullet.y < 600 and bullet.y > 0:
            bullet.y -= bullet.vel
        elif len(bullets1) > 1:
            bullets1.pop(bullets1.index(bullet))
        for enem in enemyspot:
            if bullet.x + bullet.radius > enem.hitbox[0] and bullet.x - bullet.radius < enem.hitbox[0] + \
                    enem.hitbox[2]:
                if bullet.y - bullet.radius < enem.hitbox[1] + enem.hitbox[3] and bullet.y + bullet.radius > \
                        enem.hitbox[1]:
                    enem.hit()
                    if bullet in bullets1:
                        bullets1.pop(bullets1.index(bullet))
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
