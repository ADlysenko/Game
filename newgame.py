import pygame
import random
from pygame.locals import *

pygame.init()
win = pygame.display.set_mode((400, 600))  # 600 800
font = pygame.font.SysFont("comicsans", 20, True)

pygame.display.set_caption("FarGalaxy")

bg = pygame.image.load("bg2.png")
fly = pygame.image.load("player.png")
flyr = pygame.image.load("playerr.png")
flyl = pygame.image.load("playerl.png")
ene = pygame.image.load("enemy.png")
boss1 = [pygame.image.load("boss.png"), pygame.image.load("boss2.png"), pygame.image.load("boss3.png")]
boss2 = [pygame.image.load("bossrot.png"), pygame.image.load("bossrot2.png"), pygame.image.load("bossrot3.png")]
blow = [pygame.image.load("blow1.png"), pygame.image.load("blow2.png"), pygame.image.load("blow3.png"),
        pygame.image.load("blow4.png"), pygame.image.load("blow5.png"), pygame.image.load("blow6.png")]
blowboss = [pygame.image.load("blowboss.png"), pygame.image.load("blowboss2.png"), pygame.image.load("blowboss3.png"),
            pygame.image.load("blowboss4.png"), pygame.image.load("blowboss5.png"), pygame.image.load("blowboss6.png"),
            pygame.image.load("blowboss7.png")]
gif = pygame.image.load("mainmenu1.png")
box = [pygame.image.load("box.png "), pygame.image.load("box2.png"), pygame.image.load("box3.png"),
       pygame.image.load("box4.png")]
mainmenu = pygame.image.load("mainmenu2.png")
startgame1 = pygame.image.load("start1.png")
achiev = pygame.image.load("change1.png")
quit1 = pygame.image.load("quit1.png")
pause1 = pygame.image.load("pause2.png")
pausebutton = pygame.image.load("pausebutton.png")
menubut = pygame.image.load("menubut1.png")
resumebut = pygame.image.load("resumebut1.png")
tryagain = pygame.image.load("tryagain.png")
ok = pygame.image.load("ok.png")
explosion = pygame.mixer.Sound("Explosion5.wav")
bulsound = pygame.mixer.Sound("Laser_Shoot78.wav")
power = pygame.mixer.Sound("Powerup19.wav")
hurt = pygame.mixer.Sound("Hit_Hurt63.wav")
shieldsound = pygame.mixer.Sound("Powerup22.wav")
healthsound = pygame.mixer.Sound("Powerup49.wav")
clock = pygame.time.Clock

count = a = z = score = countdamage = countbox = kill = n = timeblow = i2 = iboss = i = 0
vol = 0.5
left = False
right = False
click = False
run = True
plushealth = False
pygame.mixer.music.set_volume(vol)
nick = "Player"


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
        global plushealth
        global hel
        if self.n == 0:
            for enem in enemyspot:
                enem.health -= enem.health
        if self.n == 1:
            shieldsound.play()
            countbox = 0
            plane.damage = 0
            if len(shield) == 0:
                shield.append(shield1(self.x, self.y, 30, (0, 191, 255), 2))
        if self.n == 2:
            power.play()
            if plane.damage < 50:
                plane.damageout += 5
                countdamage = 0
        if self.n == 3:
            healthsound.play()
            plushealth = True
            if plane.health < 70:
                hel = plane.health
            else:
                hel = 70
            # if plane.health < 70:
            #     if plane.health < plane.health + 30:
            #         plane.health += 1
            # else:
            #     plane.health += (100 - plane.health)


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
        global name
        global score
        for shi in shield:
            if shi.exist:
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
        self.hitbox = (self.x, self.y, self.width, self.height)
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
        self.count += 1
        if self.count == 20:
            bulsound.play()
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
        if left:
            win.blit(flyl, (self.x, self.y))
        elif right:
            win.blit(flyr, (self.x, self.y))
        else:
            win.blit(fly, (self.x, self.y))
        pygame.draw.rect(win, (0, 191, 255), (126, 575, self.health * 1.52, 15))
        pygame.draw.rect(win, (123, 104, 238), (126, 575, 152, 15), 2)
        font1 = pygame.font.SysFont("Verdana", 15, True)
        if self.health == 100:
            text = font1.render((str(self.health) + "%"), 1, (255, 255, 255))
            win.blit(text, (70, 573))
        else:
            text = font1.render((str(self.health) + "%"), 1, (255, 255, 255))
            win.blit(text, (80, 573))

    def hitme(self):
        if self.health > 5:
            self.health -= self.damage
        else:
            list_score.append((nick, round(score)))
            file = open('bestscore', 'w')
            for ii in list_score:
                file.write(ii[0] + ' - ' + str(ii[1]) + '\n')
            file.close()
            deadplayer()


class enemy():
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
            self.count += 1
            if self.count % 60 == 0:
                bullets2.append(
                    shoot((round(self.x + self.width // 2)), round((self.y + self.height // 2) + 25), 3,
                          (255, 0, 0), -5))
                self.count = 0
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 7, 40, 5))
            pygame.draw.rect(win, (0, 100, 0), (self.hitbox[0], self.hitbox[1] - 7, 40 - (4 * (10 - self.health)), 5))

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
        for bos in bossspot:
            if bos.visible:
                if self.y > -200:
                    self.r1 = -200
                else:
                    enemyspot.pop(enemyspot.index(self))
        if self.r1 >= self.y:
            self.y += self.vel
        else:
            self.y -= self.vel
        if self.health <= 0:
            kill += 1
            blows.append(bloww(self.x, self.y))
            explosion.play()
            if self in enemyspot:
                enemyspot.pop(enemyspot.index(self))


class boss(object):
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.vel = 1
        self.r = 200
        self.r1 = 148
        self.count = 0
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.health = 500
        self.visible = True
        self.right = False
        self.left = True

    def draw(self, win):
        self.move()
        if self.visible:
            self.count += 1
            if self.count % 9 == 0:
                if self.left:
                    bullets2.append(
                        shoot(self.x + 64, self.y + 55, 3,
                              (255, 0, 0), -5))
                    bullets2.append(
                        shoot(self.x + 81, self.y + 55, 3,
                              (255, 0, 0), -5))
                    if self.health < 250:
                        bullets2.append(
                            shoot(self.x + 53, self.y + 42, 2,
                                  (255, 0, 0), -5))
                        bullets2.append(
                            shoot(self.x + 57, self.y + 42, 2,
                                  (255, 0, 0), -5))
                    self.count = 0
                if self.right:
                    bullets2.append(
                        shoot(self.x + 118, self.y + 53, 3,
                              (255, 0, 0), -5))
                    bullets2.append(
                        shoot(self.x + 135, self.y + 53, 3,
                              (255, 0, 0), -5))
                    if self.health < 250:
                        bullets2.append(
                            shoot(self.x + 140, self.y + 41, 2,
                                  (255, 0, 0), -5))
                        bullets2.append(
                            shoot(self.x + 144, self.y + 41, 2,
                                  (255, 0, 0), -5))
                    self.count = 0
            if self.left:
                win.blit(boss1[self.count // 3], (self.x, self.y))
            elif self.right:
                win.blit(boss2[self.count // 3], (self.x, self.y))
            self.hitbox = (self.x, self.y, self.width, self.height)
            # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
            pygame.draw.rect(win, (65, 105, 225), (self.hitbox[0], self.hitbox[1] - 12, (self.health // 2.5) - 2, 10))
            pygame.draw.rect(win, (123, 104, 238), (self.hitbox[0], self.hitbox[1] - 12, 198, 10), 1)

    def hit(self):
        if plane.damageout <= self.health:
            self.health -= plane.damageout
        else:
            self.health -= self.health

    def move(self):
        global kill
        if self.r == self.x:
            self.r = random.randrange(-70, 332, self.vel)
        if self.r >= self.x:
            self.x += self.vel
            self.right = True
            self.left = False
        else:
            self.x -= self.vel
            self.right = False
            self.left = True
        if self.r1 == self.y:
            self.r1 = random.randrange(30, 162, self.vel)
        if self.r1 >= self.y:
            self.y += self.vel
        else:
            self.y -= self.vel
        if self.health <= 0:
            blowbosss.append(blowwboss(self.x, self.y))
            bossspot.pop(bossspot.index(self))


class bloww():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, win):
        self.move()
        win.blit(blow[(i // 4)], (self.x, self.y))

    def move(self):
        self.y += 3


class blowwboss():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, win):
        self.move()
        win.blit(blowboss[(iboss // 4)], (self.x, self.y))

    def move(self):
        self.y += 3


def drawWindow():
    global score
    global z
    global i
    global click
    global iboss
    global plushealth
    global hel
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
    for bl in blowbosss:
        bl.draw(win)
        iboss += 1
        if iboss == 28:
            blowbosss.pop(blowbosss.index((bl)))
            iboss = 0
    for boxs in boxspot:
        boxs.draw(win)
    for enem in enemyspot:
        enem.draw(win)
    for bos in bossspot:
        bos.draw(win)
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
    if plushealth:
        if plane.health < hel + 30:
            plane.health += 1
        else:
            plushealth = False
    if countdamage < 40 and countdamage != 0:
        text = font.render(("+damage"), 1, (255, 255, 255))
        win.blit(text, (plane.hitbox[0] - 14, plane.hitbox[1] - 25))

    text = font.render("Score: " + str(int(score)), 1, (255, 255, 255))
    if score < 10:
        win.blit(text, (337, 5))
    elif score < 100:
        win.blit(text, (329, 5))
    elif score < 1000:
        win.blit(text, (320, 5))
    text = font.render("Kills: " + str(int(kill)), 1, (255, 255, 255))
    win.blit(text, (5, 5))
    win.blit(pause1, (180, 5))
    # pygame.draw.rect(win, (65, 105, 225), (290, 535, 100, 60))
    pygame.display.update()


plane = player(180, 330, 38, 38)
enemyspot = []
bossspot = []
blowbosss = []
boxspot = []
blows = []
bullets1 = []
bullets2 = []
shield = []
button_pause = pygame.draw.rect(win, (255, 0, 0), (180, 5, 30, 30))


def pause():
    global click
    global button_pause
    global run
    paused = True
    button_exit = pygame.draw.rect(win, (255, 0, 0), (140, 290, 120, 40))
    button_resume = pygame.draw.rect(win, (255, 0, 0), (140, 240, 120, 40))
    win.blit(pausebutton, (100, 210))
    win.blit(resumebut, (140, 255))
    font2 = pygame.font.SysFont("Courier New", 25, True)
    text = font2.render(("PAUSE"), 1, (255, 255, 255))
    win.blit(text, (163, 220))
    win.blit(menubut, (140, 300))
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
                menu()
        pygame.display.update()
        clock().tick(60)


def deadplayer():
    global click
    global kill
    global score
    global run
    paused = True
    button_exit = pygame.draw.rect(win, (255, 0, 0), (140, 300, 120, 40))
    button_resume = pygame.draw.rect(win, (255, 0, 0), (140, 255, 120, 40))
    win.blit(pausebutton, (100, 210))
    win.blit(tryagain, (140, 255))
    font3 = pygame.font.SysFont("Courier New", 25, True)
    text = font3.render(("YOU ARE DEAD"), 1, (255, 0, 0))
    win.blit(text, (112, 220))
    win.blit(menubut, (140, 300))

    while paused:
        click = False
        # button_e = pygame.draw.rect(win, (255, 0, 0), (100, 210, 200, 150))
        mousex, mousey = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                paused = False
                run = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        if button_resume.collidepoint((mousex, mousey)):
            if click:
                score = 0
                kill = 0
                enemyspot.clear()
                bullets1.clear()
                bullets2.clear()
                boxspot.clear()
                shield.clear()
                bossspot.clear()
                blowbosss.clear()
                blows.clear()
                plane.health = 100
                plane.x = 180
                plane.y = 650
                game()
        elif button_exit.collidepoint((mousex, mousey)):
            if click:
                menu()
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
    global vol
    pygame.mixer.music.set_volume(vol)
    pygame.mixer.music.load("OutThere.ogg")
    pygame.mixer.music.play(-1)
    while run:
        clock().tick(60)
        click = False
        if plane.y > 510 and score < 5:
            plane.y -= 2 * plane.vel
        if score > 10:
            if len(enemyspot) < 5:
                r3 = random.randrange(100, 200, 20)
                enemyspot.append(enemy(r3, -200, 40, 40, 450))
        if score > 150 and score < 155:
            if len(bossspot) == 0:
                bossspot.append(boss(-200, 150, 198, 68, 450))
        if score > 10:
            ran = random.randrange(0, 7000, 20)
            if ran == 20:
                r4 = random.randrange(0, 400, 20)
                r5 = random.randrange(-100, -200, -20)
                boxspot.append(box1(r4, r5, 24, 24))
                for box in boxspot:
                    if box.n == None:
                        box.n = random.randrange(0, 4, 1)
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
                        hurt.play()
                        enem.hit()
                        if bullet in bullets1:
                            bullets1.pop(bullets1.index(bullet))
            for bos in bossspot:
                if bullet.x + bullet.radius > bos.hitbox[0] and bullet.x - bullet.radius < bos.hitbox[0] + \
                        bos.hitbox[2]:
                    if bullet.y - bullet.radius < bos.hitbox[1] + bos.hitbox[
                        3] and bullet.y + bullet.radius > \
                            bos.hitbox[1]:
                        bos.hit()
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
                    if bullet in bullets2:
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


def menu():
    global score
    global kill
    global enemyspot
    global click
    global z
    global run
    global list_score
    global nick
    pygame.mixer.music.load("menumus.ogg")
    pygame.mixer.music.play(-1)
    active = False
    bscore = open("bestscore")
    bestscore = {}
    for line in bscore:
        name, score1 = line.split(" - ")
        bestscore[name] = int(score1)
    bscore.close()
    list_score = list(bestscore.items())
    list_score.sort(key=lambda i: i[1], reverse=True)
    while run:
        clock().tick(60)
        mousex, mousey = pygame.mouse.get_pos()
        button_1 = pygame.draw.rect(win, (255, 0, 0), (50, 120, 126, 36))
        button_2 = pygame.draw.rect(win, (255, 0, 0), (50, 200, 126, 36))
        button_3 = pygame.draw.rect(win, (0, 191, 255), (50, 160, 126, 36), 1)
        button_ok = pygame.draw.rect(win, (0, 191, 255), (180, 165, 25, 25), 1)
        win.blit(gif, (0, 0))
        font4 = pygame.font.SysFont("Courier New", 20, True)
        win.blit(pausebutton, (100, 400))
        text = font4.render((list_score[0][0] + " : " + str(list_score[0][1])), 1, (255, 255, 255))
        text1 = font4.render((list_score[1][0] + " : " + str(list_score[1][1])), 1, (255, 255, 255))
        text2 = font4.render((list_score[2][0] + " : " + str(list_score[2][1])), 1, (255, 255, 255))
        best_score = font4.render(("Best score:"), 1, (0, 191, 255))
        win.blit(text, ((200 - (text.get_width() // 2)), 440))
        win.blit(text1, ((200 - (text1.get_width() // 2)), 470))
        win.blit(text2, ((200 - (text2.get_width() // 2)), 500))
        win.blit(best_score, (135, 410))
        win.blit(mainmenu, (42, 50))
        win.blit(startgame1, (50, 120))
        win.blit(quit1, (50, 200))
        if button_1.collidepoint((mousex, mousey)):
            if click:
                score = 0
                kill = 0
                enemyspot.clear()
                bullets1.clear()
                bullets2.clear()
                boxspot.clear()
                shield.clear()
                plane.health = 100
                plane.x = 180
                plane.y = 650
                game()
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == KEYDOWN:
                if event.type == K_ESCAPE:
                    pygame.quit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                if button_1.collidepoint((mousex, mousey)):
                    score = 0
                    kill = 0
                    enemyspot.clear()
                    bullets1.clear()
                    bullets2.clear()
                    boxspot.clear()
                    shield.clear()
                    plane.health = 100
                    plane.x = 180
                    plane.y = 650
                    game()
                if button_2.collidepoint((mousex, mousey)):
                    run = False
                if button_3.collidepoint((mousex, mousey)):
                    active = True
                if button_ok.collidepoint((mousex, mousey)):
                    active = False
                    break
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        active = False
                        break
                    if event.key == pygame.K_BACKSPACE:
                        nick = nick[:-1]
                    else:
                        if len(nick) < 10:
                            nick += event.unicode
        if active == False:
            win.blit(achiev, (50, 160))
        else:
            box2 = pygame.font.SysFont("Verdana", 16, True).render(nick, True, (255, 255, 255))
            win.blit(box2, (60, 164))
            button_3 = pygame.draw.rect(win, (0, 191, 255), (50, 160, 126, 32), 1)
            win.blit(ok, (180, 162))
            button_ok = pygame.draw.rect(win, (0, 191, 255), (180, 163, 25, 25), 1)
        if run:
            pygame.display.update()


menu()
pygame.quit()
