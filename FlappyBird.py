import sys, pygame
import time
import random
pygame.init()

#Variablen
width = 500
height = 900
light_grey = (200,200,200)
bg_color = pygame.Color('grey12')
timeanfang = 0

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bird")

class Bird:
    def __init__(self, screen, posX, posY, color, radius):
        self.screen = screen
        self.color = color
        self.posX = posX
        self.posY = posY
        self.radius = radius
        self.dy = 0
        self.count = 0
        self.state = "stopped"
        self.anfangy = self.posY
        #self.draw()

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.posX, self.posY), self.radius)
    def move(self, timeanfang):
        self.count += 0
        if self.state == "down":
            timenow = time.time()
            self.dy =  1/2*9.81*(timenow - timeanfang)**2
            self.posY += self.dy
        if self.state == "up":
            self.posY -= 0.9
            currenttime = time.time()
            if currenttime - timeanfang > 0.15:
                self.state = "down"


    def clamp(self):
        if self.posY - self.radius <= 0:
            self.posY = self.radius
        elif self.posY + self.radius >= height:
            self.posY = height - self.radius

class Pipes:
    def __init__(self):
        self.width = 100
        self.posX = width + self.width//2
        self.gap = random.randint(100, 500)
        self.posY = random.randint(200, 700)

        def draw():







#Functions
def paint_back():
    screen.fill(bg_color)

#Objects
playing = True
bird = Bird(screen, 230, 600, light_grey, 10)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_SPACE]:
        bird.state = "up"
        timeanfang = time.time()

    if playing == True:
        paint_back()
        bird.clamp()
        bird.draw()
        bird.move(timeanfang)



    pygame.display.update()