import pygame
import random
import os

pygame.init()
pygame.font.init()
pygame.mixer.init()

win = pygame.display.set_mode(size = (1280, 720))
pygame.display.set_caption('Ping Pong')
clock = pygame.time.Clock()

class textOnScreen(object):

    def __init__(self, text, size, color, x, y):
        self.text = text
        self.size = size
        self.color = color
        self.x = x
        self.y = y
        self.myfont = pygame.font.SysFont('Comic Sans MS', self.size)

    def displayOnScreen(self, win, center = False):
        textsurface = self.myfont.render(self.text, True, self.color)
        if center:
            rect = textsurface.get_rect(center = (640,360))
            win.blit(textsurface,rect)
        else:
            win.blit(textsurface,(self.x, self.y))


class targetScore (object):

    def __init__(self):
        self.targetScore = '11'
        self.size = 40
        self.rect = (600, 100, 80, 50)
        self.x = self.rect[0]
        self.y = self.rect[1]
        self.width = self.rect[2]
        self.height = self.rect[3]
        self.color = (255,0,255)

    def updateTargetScore (self, score):
        self.targetScore += score
        if int(self.targetScore) < 1:
            self.targetScore = '1'

    def scoreIncrement (self, amount):
        self.targetScore = str(int(self.targetScore) + amount)
        if int(self.targetScore) < 1:
            self.targetScore = '1'

    def display(self, win):
        pygame.draw.rect(win, self.color, self.rect, 2)
        self.text = textOnScreen(self.targetScore, self.size, self.color, self.x + 3, self.y + 3)
        self.text.displayOnScreen(win)

class player(object):
    def __init__(self, x, y, width, height, color, scoreX, scoreY):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.velocity = 9
        self.score = 0
        self.scoreX = scoreX
        self.scoreY = scoreY
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, win):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface = win, color = self.color, rect = self.rect)
        self.displayScore = textOnScreen(str(self.score),  60, self.color, self.scoreX, self.scoreY)
        self.displayScore.displayOnScreen(win)

    def move(self, upKey, downKey, AI = False):

        if not AI:
            keys = pygame.key.get_pressed()
            if keys[upKey] and self.y >= blueUpperBoundary.start_pos[1]:
                self.y -= self.velocity
            if keys[downKey] and self.y + self.height <= blueLowerBoundary.start_pos[1]:
                self.y += self.velocity
        elif pong.Xdirection > 0:
            '''if pong.y < self.rect.centery and self.y >= blueUpperBoundary.start_pos[1]:
                self.y -= self.velocity
            elif pong.y > self.rect.centery and self.rect.bottom < blueLowerBoundary.start_pos[1]:
                self.y += self.velocity'''
            time = pong.Xvelocity/(player2.x - player1.x)
            tNorm = (blueUpperBoundary.start_pos[1] - blueLowerBoundary.start_pos[1])/pong.Yvelocity
            #!t1 = time to reach the first vertical border
            if pong.Ydirection > 0:
                t1 = (pong.ypos - blueUpperBoundary.start_pos[1])/pong.Yvelocity
                
                
            elif pong.Ydirection < 0:
                t1 = (blueLowerBoundary.start_pos[1] - pong.ypos)/pong.Yvelocity
            
            

    def victoryCheck(self, player):
        global gameRunning
        if self.score == int(target.targetScore):
            VictoryScreen(self.score)

class ball(object):
    def __init__(self, x, radius):
        self.x = x
        self.y = random.randint(50,670)
        self.radius = radius
        self.color = (255,255,255)
        self.Xvelocity = random.randint(2,4)
        self.Yvelocity = random.randint(1,6)
        self.Xdirection = random.choice([1,-1])
        self.Ydirection = random.choice([1,-1])

    def update(self, win):
        pygame.draw.circle(surface = win, color = self.color, center= (self.x, self.y), radius = self.radius)

class Timer:
    def __init__(self):
        self.accumulated_time = 0
        self.start_time = pygame.time.get_ticks()
        self.running = True

    def pause(self):
        if not self.running:
            raise Exception('Timer is already paused')
        self.running = False
        self.accumulated_time += pygame.time.get_ticks() - self.start_time

    def resume(self):
        if self.running:
            raise Exception('Timer is already running')
        self.running = True
        self.start_time = pygame.time.get_ticks()

    def get(self):
        if self.running:
            return (self.accumulated_time +
                    (pygame.time.get_ticks() - self.start_time))/1000
        else:
            return self.accumulated_time/1000

class borders(object):
    def __init__(self, color, start_pos, end_pos):
        self.color = color
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.width = 2

    def update(self, win):
        pygame.draw.line(surface = win, color = self.color, start_pos = self.start_pos, end_pos = self.end_pos, width = self.width)

class countDown ():
    def __init__(self):
        self.num = 3
        self.size = 100
        self.color = (255,255,255)
        self.xpos = 600
        self.ypos = 280
        self.inCountdown = False

    def start(self, win):
        self.counter = textOnScreen('3', self.size, self.color, self.xpos, self.ypos)
        for i in range(int(self.counter.text)):
            updateWin()
            self.counter.text = str(int(self.counter.text) - 1)
            pygame.time.delay(1000)
        self.inCountdown = False

class clickableImage (object):
    def __init__(self, path, x, y, xSize, ySize):
        self.path = path
        self.xSize = xSize
        self.ySize = ySize
        self.x = x
        self.y = y
        self.rect = (self.x, self.y, self.xSize, self.ySize)
        self.image = pygame.image.load(self.path)
        self.resizeImage = pygame.transform.scale(self.image, (self.xSize,self.ySize))

    def display(self, win):
        win.blit(self.resizeImage, (self.x, self.y))

def checkForVictory(player1, player2):
    if player1.score == int(target.targetScore):
        VictoryScreen(player1, 'Player 1', player2, 'Player 2')
    if player2.score == int(target.targetScore):
        VictoryScreen(player2, 'Player 2', player1, 'Player 1')

def VictoryScreen (victor, victorText, loser, loserText):

    winText = textOnScreen(victorText + ' Has won', 100, victor.color, 280, 300)
    finalScore = textOnScreen(str(victor.score) + ' - ' + str(loser.score), 60, (192,192,192), 580, 400)
    win.fill((0,0,0))
    winText.displayOnScreen(win, center = True)
    finalScore.displayOnScreen(win)
    pygame.display.update()
    pygame.time.delay(5000)
    gameRunning = False
    defineDefault()


def updateWin():
    win.fill((0,0,0))

    if not(gameRunning):
        mainScreen.displayOnScreen(win)
        target.display(win)
        targetText.displayOnScreen(win)

        targetL1img.display(win)
        targetL2img.display(win)
        targetL3img.display(win)
        targetR1img.display(win)
        targetR2img.display(win)
        targetR3img.display(win)

    else:
        player1.update(win)
        player2.update(win)
        pong.update(win)
        if gameRunning and not countDownText.inCountdown:
            gameTimer.displayOnScreen(win)

        #Target During gameplay
        targetTextDuringGameplay.displayOnScreen(win)

        #Boundaries
        blueLeftBoundary.update(win)
        blueUpperBoundary.update(win)
        blueLowerBoundary.update(win)
        redRightBoundary.update(win)
        redUpperBoundary.update(win)
        redLowerBoundary.update(win)
        midBoundary.update(win)

        #Pause Text
        if paused:
            pauseText.displayOnScreen(win)

        #Countdown
        if countDownText.inCountdown:
            countDownText.counter.displayOnScreen(win, center = True)

    pygame.display.update()

def defineDefault():
    #Objects
    player1 = player(100, 285, 15, 100, (0,0,255), 580,60)
    player2 = player(1180, 285, 15, 100, (255,0,0), 660,60)
    pong = ball(640, 5)

    #TargetScore
    #textbox loaction = (600, 100, 80, 50)
    target = targetScore()
    targetText = textOnScreen('Target Score', 40, (255,0,255), 510, 30)

    targetL1img = clickableImage(path = 'Assets/L1.png', x = 540, y = 100, xSize = 50, ySize = 50)
    targetL2img = clickableImage(path = 'Assets/L2.png', x = 450, y = 100, xSize = 60, ySize = 50)
    targetL3img = clickableImage(path = 'Assets/L3.png', x = 360, y = 100, xSize = 70, ySize = 50)
    targetR1img = clickableImage(path = 'Assets/R1.png', x = 690, y = 100, xSize = 50, ySize = 50)
    targetR2img = clickableImage(path = 'Assets/R2.png', x = 760, y = 100, xSize = 60, ySize = 50)
    targetR3img = clickableImage(path = 'Assets/R3.png', x = 840, y = 100, xSize = 70, ySize = 50)

    targetL1img.resizeImage.get_rect()
    #MainScreen
    mainScreen = textOnScreen('Click to start', 40, (255,255,255), 500, 360)

    #Counter
    countDownText = countDown()

    #Boundaries
    blueLeftBoundary = borders(player1.color, (50,50), (50,670))
    blueUpperBoundary = borders(player1.color, (50,50), (640,50))
    blueLowerBoundary = borders(player1.color, (50,670), (640,670))
    redRightBoundary = borders(player2.color, (1230,50), (1230, 670))
    redUpperBoundary = borders(player2.color, (1230,50), (640, 50))
    redLowerBoundary = borders(player2.color, (1230, 670), (640,670))
    midBoundary = borders((190,190,190), (640,50), (640,670))

    #Pause Text
    pauseText = textOnScreen('PAUSED', 100, (255,255,255), 450, 300)

    #Load Music
    music_folder = 'D:/More Python Projects/Games/Ping Pong/Music'
    musicList = os.listdir(music_folder)
    random.shuffle(musicList)
    pygame.mixer.music.load(music_folder + '/' + musicList[0] )
    for i in musicList:
        if i == musicList[0]:
            pygame.mixer.music.load(music_folder + '/' + i)
        else:
            pygame.mixer.music.queue(music_folder + '/' + i)

    run = True
    gameRunning = False
    paused = False
    inCountdown = False
    activate_typing = False
    timesExpended = []

    globals().update(locals())

defineDefault()

while run:

    #Time delay between loops
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN and not(gameRunning):
            if pygame.Rect(target.rect).collidepoint(event.pos):
                target.targetScore = ''
                activate_typing = True
            elif pygame.Rect(targetL1img.rect).collidepoint(event.pos):
                target.scoreIncrement(-1)
            elif pygame.Rect(targetL2img.rect).collidepoint(event.pos):
                target.scoreIncrement(-5)
            elif pygame.Rect(targetL3img.rect).collidepoint(event.pos):
                target.scoreIncrement(-10)
            elif pygame.Rect(targetR1img.rect).collidepoint(event.pos):
                target.scoreIncrement(1)
            elif pygame.Rect(targetR2img.rect).collidepoint(event.pos):
                target.scoreIncrement(5)
            elif pygame.Rect(targetR3img.rect).collidepoint(event.pos):
                target.scoreIncrement(10)

            else:
                activate_typing = False
                countDownText.inCountdown = True
                gameRunning = True
                targetTextDuringGameplay = textOnScreen('Target :' +target.targetScore, 40, (173,255,47), 1000, 0)
                countDownText.start(win)
                time = Timer()
                gameTimer = textOnScreen(str(time.get()), 30, (255,255,255), 600, 0)

        if event.type == pygame.KEYDOWN and activate_typing:
            if event.key == pygame.K_BACKSPACE:
                target.targetScore = target.targetScore[ : -1]
            elif event.unicode.isnumeric():
                target.updateTargetScore(event.unicode)

    if gameRunning and not countDownText.inCountdown:
        keys = pygame.key.get_pressed()
        #Pause the game
        if keys[pygame.K_ESCAPE]:
            if not(paused):
                time.pause()
                paused = not(paused)
                pygame.mixer.music.pause()
            else:
                time.resume()
                paused = not(paused)
                countDownText.inCountdown = True
                countDownText.start(win)

            pygame.time.delay(1000)

        if not(paused):

            #Playing music
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.set_volume(0.7)
                pygame.mixer.music.play()

            #move the players
            player1.move(pygame.K_w, pygame.K_s)
            player2.move(pygame.K_UP, pygame.K_DOWN, AI = True)

            #Ball movements

            #Detecting collitions
            #With Top and Lower  Boundaries
            if pong.y >= blueLowerBoundary.start_pos[1] or pong.y <= blueUpperBoundary.start_pos[1]:
                pong.Ydirection *= -1

            #With left and right boundaries
            #left boundary
            if pong.x <= blueLeftBoundary.start_pos[0]:
                player2.score += 1
                checkForVictory(player1, player2)

            if pong.x >= redRightBoundary.start_pos[0]:
                player1.score += 1
                checkForVictory(player1, player2)

            if pong.x <= blueLeftBoundary.start_pos[0] or pong.x >= redRightBoundary.start_pos[0]:
                pong.x = 640
                pong.color = (255,255,255)
                pong.y = random.randint(50,670)
                pong.Xdirection = random.choice([1,-1])
                pong.Ydirection = random.choice([1,-1])
                pong.Xvelocity = random.randint(2,4)
                pong.Yvelocity = random.randint(1,6)
                time.accumulated_time = 0
                time.start_time = pygame.time.get_ticks()
                timesExpended = []


            #with players
            if pong.x in range(player1.x  + player1.width - 7, player1.x + player1.width + 7) and pong.y in range(player1.y, player1.y + player1.height + 5):
                pong.Xdirection *= -1
                pong.color = player1.color


            if pong.x in range(player2.x - 7, player2.x + 7) and pong.y in range(player2.y, player2.y + player2.height + 5):
                pong.Xdirection *= -1
                pong.color = player2.color


            #Increasing velocity every 5 seconds
            if (time.get()//1) % 5 == 0 and (time.get()//1) not in timesExpended:
                timesExpended.append(time.get()//1)
                pong.Xvelocity += random.randint(-1,3)
                pong.Yvelocity += random.randint(-1,3)

            #Changing trajectory every 20 seconds
            #CODE TO BE ADDED#

            pong.x += pong.Xvelocity * pong.Xdirection
            pong.y += pong.Yvelocity * pong.Ydirection

            #Updating time
            gameTimer.text = str(time.get())

    updateWin()

pygame.quit()
