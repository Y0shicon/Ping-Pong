import pygame
import random

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

	def displayOnScreen(self, win):
		textsurface = self.myfont.render(self.text, True, self.color)
		win.blit(textsurface,(self.x,self.y))


class player(object):
	def __init__(self, x, y, width, height, color, scoreX, scoreY):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.color = color
		self.velocity = 8
		self.score = 0
		self.scoreX = scoreX
		self.scoreY = scoreY

	def update(self, win):
		pygame.draw.rect(surface = win, color = (255,255,255), rect = (self.x, self.y, self.width, self.height))
		self.displayScore = textOnScreen(str(self.score),  60, self.color, self.scoreX, self.scoreY)
		self.displayScore.displayOnScreen(win)

	def move(self, upKey, downKey, leftKey, rightKey):
		keys = pygame.key.get_pressed()
		if keys[upKey] and self.y >= blueUpperBoundary.start_pos[1]:
			self.y -= self.velocity
		if keys[downKey] and self.y + self.height <= blueLowerBoundary.start_pos[1]:
			self.y += self.velocity
		'''if keys[leftKey] :
									self.x -= self.velocity
								if keys[rightKey] :
									self.x += self.velocity 
						'''

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
		self.inCountdown = True
		self.counter = textOnScreen('3', self.size, self.color, self.xpos, self.ypos)
		for i in range(int(self.counter.text)):
			updateWin()
			self.counter.text = str(int(self.counter.text) - 1)
			pygame.time.delay(1000)
		self.inCountdown = False

def updateWin():
	win.fill((0,0,0))
	
	player1.update(win)
	player2.update(win)
	pong.update(win)
	if gameRunning:
		gameTimer.displayOnScreen(win)
	
	#Countdown
	if countDownText.inCountdown:
		countDownText.counter.displayOnScreen(win)

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

	pygame.display.update()

#Objects
player1 = player(100, 285, 15, 100, (0,0,255), 600,60)
player2 = player(1180, 285, 15, 100, (255,0,0), 640,60)
pong = ball(640, 5)

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

run = True
gameRunning = False
paused = False
timesExpended = []
while run:

	#Time delay between loops
	clock.tick(60)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN and not(gameRunning):
			countDownText.start(win)
			gameRunning = True
			time = Timer()
			gameTimer = textOnScreen(str(time.get()), 30, (255,255,255), 600, 0)			

	if gameRunning:
		keys = pygame.key.get_pressed()
		#Pause the game
		if keys[pygame.K_ESCAPE]:
			if not(paused):
				time.pause()
				paused = not(paused)
			else:
				time.resume()
				paused = not(paused)
				countDownText.start(win)

			pygame.time.delay(1000)

		if not(paused):		
			#move the players
			player1.move(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d)
			player2.move(pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT,  pygame.K_RIGHT)	

			#Playing music
			pygame.mixer.music.play()

			#Ball movements

			#Detecting collitions
			#With Top and Lower  Boundaries
			if pong.y >= blueLowerBoundary.start_pos[1] or pong.y <= blueUpperBoundary.start_pos[1]:
				pong.Ydirection *= -1 

			#With left and right boundaries
			#left boundary
			player2.score += 1 if pong.x <= blueLeftBoundary.start_pos[0] else 0
			#right boundary
			player1.score += 1 if pong.x >= redRightBoundary.start_pos[0] else 0
			
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
				pong.Xvelocity += 1
				pong.Yvelocity += 1

			#Changing trajectory every 20 seconds
			#CODE TO BE ADDED#

			pong.x += pong.Xvelocity * pong.Xdirection
			pong.y += pong.Yvelocity * pong.Ydirection

			#Updating time
			gameTimer.text = str(time.get())

		else:
			pass

		updateWin()


	else:
		mainScreen = textOnScreen('Click to start', 40, (255,255,255), 500, 360)
		mainScreen.displayOnScreen(win)
		pygame.display.update()

pygame.quit()
