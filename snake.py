import pygame
from pygame.locals import *
import sys
import random
from collections import deque
     
class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.surf = pygame.Surface((blockSize, blockSize))
        self.surf.fill(SNAKECOLOR)
        self.rect = self.surf.get_rect(center = (centre, centre))
        self.position = [centre, centre]
        self.length = 2
        self.body=deque([self.position])
        self.rects = []
        self.priorPosition=[]
        
    def updateLength(self):
        self.length+=1
        print('length increased to',self.length)

    def drawSnake(self):
        rects = []
        for idx,block in enumerate(self.body):
            rects.append(self.surf.get_rect(center = block))
            if isStopped==False:
                self.rect = self.surf.get_rect(center = self.position)
        self.rects = rects
    def reset(self):
        global score
        
        self.surf = pygame.Surface((blockSize, blockSize))
        self.surf.fill(SNAKECOLOR)
        self.rect = self.surf.get_rect(center = (centre, centre))
        self.position = [centre, centre]
        self.length = 2
        self.body=deque([self.position])
        self.rects = []
        self.priorPosition=[]
        FPS=5
        score = 0
        
        
class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((blockSize, blockSize))
        self.surf.fill((255,255,0))
        self.rect = self.surf.get_rect(center = (centre-2*blockSize, centre-2*blockSize))
        self.position = [centre-2*blockSize, centre-2*blockSize]
        self.ColliderSize = 0.5*blockSize
        
    def reset(self):
        self.surf = pygame.Surface((blockSize, blockSize))
        self.surf.fill((255,255,0))
        self.rect = self.surf.get_rect(center = (centre-2*blockSize, centre-2*blockSize))
        self.position = [centre-2*blockSize, centre-2*blockSize]
        self.ColliderSize = 0.5*blockSize

def drawGrid():
    for x in range(0, gridSize):
        for y in range(0, gridSize):
            rect = pygame.Rect(x*blockSize, y*blockSize, blockSize, blockSize)
            pygame.draw.rect(SCREEN, WHITE, rect, 1)
            
def updateSnakePosition(direction,sprite):
    global isStopped
    
    #update first body position
    priorPosition = [sprite.position[0],sprite.position[1]]
    isStopped=False
    
    #update head position:
    if direction == 'right':
        if sprite.position[0]>WIDTH-(blockSize):
            isStopped=True
            pass
        else:
            sprite.position[0] += directions[direction][0]*blockSize
    if direction == 'left':
        if sprite.position[0]<0+(blockSize):
            isStopped=True
            pass
        else:
            sprite.position[0] += directions[direction][0]*blockSize       
    if direction == 'down':
        if sprite.position[1]>WIDTH-(blockSize):
            isStopped=True
            pass
        else:
            sprite.position[1] += directions[direction][1]*blockSize
    if direction == 'up':
        if sprite.position[1]<0+(blockSize):
            isStopped=True
            pass
        else:
            sprite.position[1] += directions[direction][1]*blockSize
            
    #update the body with new position and pop out the last position
    if isStopped == False:
        snake.body.appendleft(priorPosition)
        if snake.length<=len(snake.body):
            snake.body.pop()
    sprite.drawSnake()

                
def updateFoodPosition(sprite):
    newCoords = (random.randint(1,gridSize),random.randint(1,gridSize))

    for idx, block in enumerate(snake.body):
        blockCoords = (int((block[0]+blockSize/2)/blockSize),int((block[1]+blockSize/2)/blockSize))
        
        while newCoords == blockCoords:
            print('reassigning coordinates...')
            newCoords = (random.randint(1,gridSize),random.randint(1,gridSize))
    
    for idx, position in enumerate(sprite.position):
        sprite.position[idx] = newCoords[idx]*blockSize-(blockSize/2)
        sprite.rect = sprite.surf.get_rect(center = sprite.position)
        
def checkForCollision(snake,food):
    global FPS
    global score
    
    foodBoundariesX = [food.position[0]+food.ColliderSize, food.position[0]-food.ColliderSize]
    foodBoundariesY = [food.position[1]+food.ColliderSize, food.position[1]-food.ColliderSize]
    if foodBoundariesX[0]>=snake.position[0] and foodBoundariesX[1]<=snake.position[0]:
        if foodBoundariesY[0]>=snake.position[1] and foodBoundariesY[1]<=snake.position[1]:
            print('Collision detected...')
            updateFoodPosition(food)
            snake.updateLength()
            FPS+=0.2
            score+=1
            
def checkForGameOver():
    for block in snake.body:
        if abs(block[0]-snake.position[0])<blockSize/2 and abs(block[1]-snake.position[1])<blockSize/2 and snake.length != 2:
            isStopped == False
            onGameOver()
            break
        elif isStopped == True:
            isStopped == False
            onGameOver()
            break

                
def onGameOver():
    global isGameOver
    print('GAMEOVER')
    isGameOver=True
    
    while isGameOver:
        text = FONT.render("Press space bar to play again:", True, WHITE)            
        textRect = text.get_rect(center = (centre,centre))
        scoreText = FONT.render("Score: {}".format(score), True, WHITE)
        scoreTextRect = text.get_rect(center = (centre,centre-blockSize*2))
        SCREEN.blit(text, textRect)
        SCREEN.blit(scoreText, scoreTextRect)
        CLOCK.tick(100)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    isGameOver = False
                    snake.reset()
                    food.reset()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                    


    

def main():
    global CLOCK
    global SCREEN
    global HEIGHT
    global WIDTH
    global FPS
    global FONT
    global blockSize
    global gridSize
    global direction
    global directions
    global centre
    global BLACK
    global WHITE
    global SNAKECOLOR
    global snake
    global food
    global isStopped
    global isGameOver
    global score
    
    #change settings here 
    HEIGHT = 400
    WIDTH = 400
    FPS = 5
    
    direction='left'
    directions = {'left':[-1,0],'right':[1,0],'up':[0,-1],'down':[0,1]}
    gridSize = 20
    blockSize = HEIGHT/gridSize
    centre = int(gridSize/2)*blockSize-blockSize/2

    #define color rgb values for easy access
    BLACK = (0, 0, 0)
    WHITE = (200, 200, 200)
    SNAKECOLOR = (128,255,40)
    isStopped = False
    isRunning=True
    isGameOver=False
    score = 0
    pygame.init()
    vec = pygame.math.Vector2  # 2 for two dimensional

    CLOCK = pygame.time.Clock()
    FONT = pygame.font.Font('freesansbold.ttf', 20) 
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake")
    #create sprites from classes
    food = Food()
    snake = Snake()


    all_sprites = pygame.sprite.Group()
    all_sprites.add(food)
    all_sprites.add(snake)
    
     
    while True:
        SCREEN.fill((0,0,0))
        #drawGrid()
                #get the pressed key
        keysPressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                keysPressed = pygame.key.get_pressed()
        # if right arrow key is pressed 
                if keysPressed[pygame.K_RIGHT] and direction != 'left': 
                    print('moving right...')
                    direction = 'right'
         # if left arrow key is pressed 
                if keysPressed[pygame.K_LEFT] and direction != 'right': 
                    print('moving left...')
                    direction = 'left'
        # if down arrow key is pressed 
                if keysPressed[pygame.K_DOWN] and direction != 'up': 
                    print('moving down...')
                    direction = 'down'
        # if up arrow key is pressed 
                if keysPressed[pygame.K_UP] and direction != 'down': 
                    print('moving up...')
                    direction = 'up'
                
        checkForGameOver()
        
        if isGameOver==False:
            updateSnakePosition(direction, snake)
            
        
        for entity in all_sprites:
            SCREEN.blit(entity.surf, entity.rect)
        for rect in snake.rects:
            SCREEN.blit(snake.surf,rect)

        checkForCollision(snake,food)
        pygame.display.update()
        CLOCK.tick(FPS)
main()
