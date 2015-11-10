# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

#KRT 14/06/2012 modified Start Screen and Game Over screen to cope with mouse events
#KRT 14/06/2012 Added a non-busy wait to Game Over screen to reduce processor loading from near 100%
import random, pygame, sys
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 1280 
WINDOWHEIGHT =  960
BALLSIZE = (100,100)

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
VERYDARKGRAY = (10, 10, 10)
PINK      = (255, 155, 155)
DARKBLUE  = (  0,   0, 155)
FLASHCOLOR = (255, 255, 255)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('PingPong!')
    pygame.key.set_repeat(10,10)

    showStartScreen()
    latestScore = (0,0)
    while True:
        latestScore = runGame(latestScore)
	if latestScore[0] == 10 or latestScore[1] == 10:
		latestScore = (0,0)
        	showGameOverScreen()


def runGame(scores):
        bat1 = Bat(20, 10)
        bat2 = Bat(WINDOWWIDTH - 50, WINDOWHEIGHT - 210)
 	ball = Ball(100,100)
        while True:
		checkCollision(ball, bat1, bat2)
		ball.move()
		score = ball.checkScore()
		if score == 1:
			return (scores[0], scores[1] + 1)	
		elif score == -1:	
			return (scores[0] + 1, scores[1])
                checkForKeyPress()
		keys = pygame.key.get_pressed()
		if keys[K_UP]:
			bat2.move(-20)
		elif keys[K_DOWN]:
			bat2.move(20)
   
		if keys[K_q]:
			bat1.move(-20)
		elif keys[K_a]:
			bat1.move(20)

        	DISPLAYSURF.fill(BGCOLOR)
		ball.draw(DISPLAYSURF)
		drawBats(bat1, bat2)
		drawScores(scores[0], scores[1])
        	pygame.display.update()
        	FPSCLOCK.tick(FPS)

def checkKeyPresses():
	for event in pygame.event.get():
		if event.type == QUIT:
			terminate()

def checkCollision(ball, bat1, bat2):
        ballRect = ball.rect().move(ball.dx, ball.dy)
        
	if ballRect.colliderect(bat1.rect()) or ballRect.colliderect(bat2.rect()):	
		ball.dx = -ball.dx + random.randint(-2,2)
		ball.dy = -ball.dy + random.randint(-2,2)

def drawScores(score1, score2):
    scoreFont = pygame.font.Font('freesansbold.ttf', 100)
    score1Surf = scoreFont.render(str(score1), True, WHITE)
    score2Surf = scoreFont.render(str(score2), True, WHITE)

    DISPLAYSURF.blit(score1Surf, pygame.Rect(100,100,100,100))
    DISPLAYSURF.blit(score2Surf, pygame.Rect(WINDOWWIDTH - 200,100,100,100))

class Ball():

   def __init__(self, x, y):
	self.x = x
	self.y = y
 	self.dx = 10
	self.dy = -20
	self.width = 50
	self.height = 50
	
   def draw(self, surface):
        ballRect = pygame.Rect(self.x,self.y, self.width,self.height)
        pygame.draw.rect(surface, WHITE, ballRect)

   def move(self):
	self.x = self.x + self.dx 
	self.y = self.y + self.dy
 	if self.y < 0:
		self.y = self.y - self.dy
		self.dy = -self.dy
	elif (self.y + self.height) > WINDOWHEIGHT:
		self.y = self.y - self.dy
		self.dy = -self.dy

   def checkScore(self):
	if self.x < 0:
		return 1
	elif self.x > WINDOWWIDTH:
		return -1
        else:
		return 0	

   def rect(self):
	return pygame.Rect(self.x, self.y, self.width, self.height)

class Bat():

    def __init__(self, x,y):
	self.x = x
	self.y = y
	self.height = 200
	self.width = 30
	 
    def draw(self, surface):
    	rect = pygame.Rect(self.x,self.y, self.width, self.height)
    	pygame.draw.rect(surface, WHITE, rect) 		

    def move(self, dy):
	if (self.y + dy > 0) and (self.y + dy + self.height < WINDOWHEIGHT):
		self.y = self.y + dy	

    def rect(self):
	return pygame.Rect(self.x, self.y, self.width, self.height)
	
	
def drawBats(bat1, bat2):
    bat1.draw(DISPLAYSURF)
    bat2.draw(DISPLAYSURF)

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)



# KRT 14/06/2012 rewrite event detection to deal with mouse use
def checkForKeyPress():
    for event in pygame.event.get():
        if event.type == QUIT:      #event is quit 
            terminate()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:   #event is escape key
                terminate()
            else:
                return event.key   #key found return with it
    # no quit or key events in queue so return None    
    return None

    
def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Ella!', True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render('Alex!', True, GREEN)

    degrees1 = 0
    degrees2 = 0
    
#KRT 14/06/2012 rewrite event detection to deal with mouse use
    pygame.event.get()  #clear out event queue
    
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()
#KRT 14/06/2012 rewrite event detection to deal with mouse use
        if checkForKeyPress():
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()



def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
#KRT 14/06/2012 rewrite event detection to deal with mouse use
    pygame.event.get()  #clear out event queue 
    while True:
        if checkForKeyPress():
            return
#KRT 12/06/2012 reduce processor loading in gameover screen.
        pygame.time.wait(100)

def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


if __name__ == '__main__':
    main()
