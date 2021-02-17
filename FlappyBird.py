import sys, pygame
import time
import random
from Klassen_Flappy_Bird import *

#Pygame initialiseren
pygame.init()
clock = pygame.time.Clock()

#Variablen
width = 500
height = 900
light_grey = (200,200,200)
bg_color = pygame.Color('grey12')

#Screen Setup
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bird")

#Functions
def paint_back():
    screen.fill(bg_color)

#Variablen
clock.tick(60)
playing = False

#Objects
bird = Bird(screen, 230, light_grey, 15)
pipes = []
collision = CollisionManager()
score1 = Score(screen, "0", 50, 15, light_grey)
score1copy = Score(screen, "0", 250, 100, light_grey)
highscore = Score(screen, "0", 250, 280,light_grey)
ausgabeh = Textausagbe(screen, 250, 200, light_grey,"Highscore")
ausgabes = Textausagbe(screen, 250, 30, light_grey, "Score")
playbutton = Button(screen, light_grey, 200, 400, 100, 50, "Play")

#Main-Game-Loop
while True:
    for event in pygame.event.get():
        #Speichert Maus Position in pos
        pos = pygame.mouse.get_pos()
        #Exit wenn rotes Kreuz gedrückt wird
        if event.type == pygame.QUIT:
            sys.exit()
        #Event Mousebutton down
        if event.type == pygame.MOUSEBUTTONDOWN:
            #Mouse Button über Play Button down
            if playbutton.isOver(pos) and playbutton.state == "visible":
                #Erstelle drei Pipes als Buffer
                pipes.append(Pipes(screen, light_grey,random.randint(100, 600), random.randint(250, 350), 900))
                #Restarte Score oben links
                score1.restart()
                #Restarte Score in Mitte für Playing = False screen
                score1copy.restart()
                playing = True

    keys_pressed = pygame.key.get_pressed()
    #Wenn Leertaste gedrückt rufe up zum nach oben fliegen auf
    if keys_pressed[pygame.K_SPACE]:
        bird.up()

    if playing == True:
        #Schwarzer Hintergrund
        paint_back()
        for pipe in pipes:
            pipe.move()
            pipe.draw()
            if pipe.collide(bird):
                playing = False
            if pipe.state == "out":
                del pipes[0:1]
            if pipe.append():
                pipes.append(Pipes(screen, light_grey, random.randint(0, 700), random.randint(200, 300), 900))
            if pipe.points(bird):
                score1.increase()
        if collision.bird_floors(bird):
            playing = False
        playbutton.state = "unvisible"
        #Score drawen
        score1.draw()
        #Bird update und draw
        bird.update()
        bird.draw()

    #Wenn playing = False
    if playing == False:
        playbutton.state = "visible"
        #Wenn Score höher wie bisheriger Highscore setze neuen Highscore
        if int(score1.points) > int(highscore.points):
            highscore.points = score1.points
        #Score für Mitte von Spielscore copyen
        score1copy.points = score1.points
        score1copy.set()
        #Highscore setzen
        highscore.set()
        paint_back()
        #Scores und Ausgaben, Button drawen
        score1copy.draw()
        highscore.draw()
        ausgabeh.draw()
        ausgabes.draw()
        playbutton.draw(screen)
        #Bird Position resetten
        bird.restart()
        pipes = []



    #Display updaten
    pygame.display.update()