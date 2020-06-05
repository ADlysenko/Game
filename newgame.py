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
box = [pygame.image.load("box.png"), pygame.image.load("box2.png"), pygame.image.load("box3.png"),
       pygame.image.load("box4.png")]
pause1 = pygame.image.load("pause2.png")
pausebutton = pygame.image.load("pausebutton.png")
menubut = pygame.image.load("menubut.png")
resumebut = pygame.image.load("resumebut.png")
clock = pygame.time.Clock

count = z = 0
a = 0
score, kill = 0, 0
right = False
left = False
run = True
i = 0
n = 0
countbox = 0
countdamage = 0


class shoot():
    def __init__(self, x, y, radius, color, vel):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel = vel

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

class shield1():
    def __init__(self, x, y, radius, color, nonrad):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel = 8
        self.nonrad = nonrad
        self.exist = True

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius, self.nonrad)

class box1():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 2
        self.color = (0, 0, 255)
        self.radius = 10
        self.n = None
        self.up = 0
        self.hitbox = (self.x, self.y, self.width, self.height)

    def draw(self, win):
        win.blit(box[self.n], (self.x, self.y))
        self.hitbox = (self.x, self.y, self.width, self.height)
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def touch(self):
        global countbox
        global countdamage
        print("YEAH")
        if self.n == 0:
            for enem in enemyspot:
                enem.health -= enem.health
        if self.n == 1:
            countbox = 0
            plane.damage = 0
            if len(shield) == 0:
                shield.append(shield1(self.x, self.y, 30, (0, 191, 255), 2))
        if self.n == 2:
            if plane.damage < 50:
                plane.damageout += 5
                countdamage = 0
        if self.n == 3:
            if plane.health < 70:
                plane.health += 30
            else:
                plane.health += (100 - plane.health)



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
        self.xbox = 580

    def draw(self, win):
        global countbox
        global countdamage
        for shi in shield:
            if shi.exist == True:
                if countbox < 300:
                    countbox += 1
                else:
                    self.damage = 5
                    for shi in shield:
                        shi.exist = False
                    countbox = 0
        if self.damageout > 5:
            if countdamage < 300:
                countdamage += 1
                if len(shield) > 0 and self.xbox == 580:
                    self.xbox -= 25
                elif len(shield) == 0 and self.xbox < 580:
                    self.xbox += 5
                font = pygame.font.SysFont("comicsans", 15, True)
                text = font.render(("+damage"), 1, (0, 191, 255))
                win.blit(text, (10, self.xbox - 10))
                pygame.draw.rect(win, (0, 191, 255), (10, self.xbox, 50, 10), 1)
                pygame.draw.rect(win, (0, 191, 255), (10, self.xbox, (300 - countdamage) // 6, 10))
            else:
                countdamage = 0
                plane.damageout = 5
        win.blit(fly, (self.x, self.y))
        self.hitbox = (self.x, self.y, self.width, self.height)
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
        self.count += 1
        if self.count % 20 == 0:
            bullets1.append(
                shoot((round(self.x + self.width // 2)), round((self.y + self.height // 2) - 25), 3,
                      (0, 255, 0), 20))
            self.count = 0
        if countbox > 0:
            font = pygame.font.SysFont("comicsans", 15, True)
            text = font.render(("shield"), 1, (0, 191, 255))
            win.blit(text, (10, 570))
            pygame.draw.rect(win, (0, 191, 255), (10, 580, 50, 10), 1)
            pygame.draw.rect(win, (0, 191, 255), (10, 580, (300 - countbox) // 6, 10))
        win.blit(fly, (self.x, self.y))
        pygame.draw.rect(win, (0, 191, 255), (126, 575, self.health * 1.52, 15))
        pygame.draw.rect(win, (123, 104, 238), (126, 575, 152, 15), 2)
        font = pygame.font.SysFont("Verdana", 15, True)
        if self.health == 100:
            text = font.render((str(self.health) + "%"), 1, (255, 255, 255))
            win.blit(text, (70, 573))
        else:
            text = font.render((str(self.health) + "%"), 1, (255, 255, 255))
            win.blit(text, (80, 573))

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
    for boxs in boxspot:
        boxs.draw(win)
    for enem in enemyspot:
        enem.draw(win)
    for bullet in bullets1:
        bullet.draw(win)
    for bullet in bullets2:
        bullet.draw(win)
    for shi in shield:
        shi.x = plane.x + 19
        shi.y = plane.y + 19
        if countbox < 250:
            if countbox < 40 and countbox != 0:
                text = font.render(("+shield"), 1, (255, 255, 255))
                win.blit(text, (plane.hitbox[0] - 8, plane.hitbox[1] + 55))
            shi.draw(win)
        elif countbox > 200 and countbox < 300:
            if countbox % 10 == 0:
                shi.draw(win)
        if shi.exist == False:
            shield.pop(shield.index(shi))
    if countdamage < 40 and countdamage != 0:
        text = font.render(("+damage"), 1, (255, 255, 255))
        win.blit(text, (plane.hitbox[0] - 14, plane.hitbox[1] + 55))
    text = font.render("Score: " + str(int(score)), 1, (255, 255, 255))
    win.blit(text, (315, 5))
    text1 = font.render("Kills: " + str(int(kill)), 1, (255, 255, 255))
    win.blit(text1, (5, 5))
    pygame.display.update()


plane = player(180, 650, 38, 38)
enemyspot = []
boxspot = []
bullets1 = []
bullets2 = []
shield = []
blows = []
button_pause = pygame.draw.rect(win, (255, 0, 0), (180, 5, 30, 30))


def pause():
    global click
    global button_pause
    global run
    paused = True
    button_exit = pygame.draw.rect(win, (255, 0, 0), (140, 290, 120, 40))
    button_resume = pygame.draw.rect(win, (255, 0, 0), (140, 240, 120, 40))
    win.blit(pausebutton, (100, 210))
    win.blit(resumebut, (140, 240))
    font = pygame.font.SysFont("comicsans", 20, True)
    text = font.render(("PAUSE"), 1, (255, 255, 255))
    win.blit(text, (175, 220))
    win.blit(menubut, (140, 290))
    while paused:
        click = False
        # button_e = pygame.draw.rect(win, (255, 0, 0), (100, 210, 200, 150))
        mousex, mousey = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                paused = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        if button_resume.collidepoint((mousex, mousey)):
            if click:
                paused = False
        elif button_exit.collidepoint((mousex, mousey)):
            if click:
                pass
        pygame.display.update()
        clock().tick(60)

def game():
    global button_pause
    global score
    global right
    global left
    global n
    global click
    global run
    while run:
        clock().tick(60)
        click = False
        if plane.y > 510 and score < 5:
            plane.y -= 2 * plane.vel
        if score > 1000:
            if len(enemyspot) < 5:
                r3 = random.randrange(100, 200, 20)
                enemyspot.append(enemy(r3, -200, 40, 40, 450))
        if score > 10:
            ran = random.randrange(0, 1000, 20)  # 7000
            if ran == 20:
                r4 = random.randrange(0, 400, 20)
                r5 = random.randrange(-100, -200, -20)
                boxspot.append(box1(r4, r5, 24, 24))
                for box in boxspot:
                    if box.n == None:
                        box.n = random.randrange(0, 4, 1)  # 0,2,1
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
        for boxs in boxspot:
            if boxs.y < 600:
                boxs.y += boxs.vel
            else:
                boxspot.pop(boxspot.index(boxs))
            if boxs.hitbox[0] + boxs.hitbox[2] > plane.hitbox[0] and boxs.hitbox[0] < plane.hitbox[0] + plane.hitbox[2]:
                if boxs.hitbox[1] < plane.hitbox[1] + plane.hitbox[3] and boxs.hitbox[1] + boxs.hitbox[3] > \
                        plane.hitbox[1]:
                    boxs.touch()
                    boxspot.pop(boxspot.index(boxs))
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
        mousex, mousey = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pause()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
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
        if button_pause.collidepoint((mousex, mousey)):
            if click:
                pause()
        score += 0.1
        if run:
            drawWindow()


game()
pygame.quit()