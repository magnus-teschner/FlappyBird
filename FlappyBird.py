import sys, pygame
import time
import random

#Pygame initialiseren
pygame.init()

#Variablen
width = 500
height = 900
light_grey = (200,200,200)
bg_color = pygame.Color('grey12')

#Screen Setup
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bird")


class Bird:
    def __init__(self, screen, posX, color, radius):
        self.screen = screen
        self.color = color
        self.posX = posX
        self.posY = height //2
        self.gravity = 0.0008
        self.lift = -0.38
        self.velocity = 0
        self.radius = radius

    #Zeichnet Bird als Kreis
    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.posX, self.posY), self.radius)

    #Ändert Bird Richtungsparameter
    def up(self):
        self.velocity = self.lift

    #Updatet Position von Bird
    def update(self):
        self.velocity += self.gravity
        self.posY += self.velocity

        if self.posY >= height - self.radius:
            self.posY = height - self.radius
            self.velocity = 0

        if self.posY - self.radius <= 0:
            self.posY = 0 + self.radius
            self.velocity = 0
    #Restartet Position von Bird bei playing = False
    def restart(self):
        self.posX = 100 #230
        self.posY = height // 2

class Pipes:
    def __init__(self, screen, color, height, gap, posX):
        self.color = color
        self.screen = screen
        self.width = 50
        self.posX = posX
        self.gap = gap
        self.posY = 0
        self.height = height
        self.state = "in"

    #Malt obere und untere Hälfte getrennt voneinander aber mit gleichen X Koordinaten
    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.posX, self.posY, self.width, self.height))
        pygame.draw.rect(self.screen, self.color, (self.posX, self.posY + self.height + self.gap, self.width, 900 - self.height - self.gap))

    #Moved pipes über Screen
    def move(self):
        self.posX -= 0.3

        #Wenn Pipe zur Hälfte aus Bild raus ändere Status zu out
        if self.posX < 0 - 25:
            self.state = "out"


class CollisionManager:

    #Checked ob Bird Floor berührt
    def bird_floors(self, bird):
        if bird.posY + bird.radius > 899 or bird.posY - bird.radius < 1:
            return True

    #checked ob bird pipes berührt
    def bird_pipes(self, pipe, bird):
        if bird.posY - bird.radius <= pipe.height or bird.posY + bird.radius >= pipe.height + pipe.gap:
            if bird.posX - bird.radius >= pipe.posX and bird.posX + bird.radius <= pipe.posX + pipe.width:
                return True

    #Checkt ob Pipe an Bird vorbei ohne Berührung
    def points(self, bird, pipe):
        if pipe.posX + pipe.width < bird.posX -15 and pipe.posX + pipe.width > bird.posX -15.3:
            return True


class Score:
    def __init__(self, screen, points, posX, posY, color):
        self.screen = screen
        self.color = color
        self.points = points
        self.posX = posX
        self.posY = posY
        self.font = pygame.font.SysFont("monospace", 80, bold = True)
        self.label = self.font.render(self.points, 0, self.color )
        self.draw()

    #Label zeichnen
    def draw(self):
        self.screen.blit(self.label, (self.posX - self.label.get_rect().width // 2, self.posY))

    #Punkte erhöhen und Label neu rendern
    def increase(self):
        points = int(self.points) + 1
        self.points = str(points)
        self.label = self.font.render(self.points, 0, light_grey)

    #Punkte auf null und neu rendern
    def restart(self):
        self.points = "0"
        self.label = self.font.render(self.points, 0, light_grey)

    #Punkte von anderer Quelle aktualisiert übernehmen
    def set(self):
        self.label = self.font.render(self.points, 0, light_grey)

class Textausagbe:
    def __init__(self, screen, posX, posY, color, text):
        self.screen = screen
        self.color = color
        self.text = text
        self.posX = posX
        self.posY = posY
        self.font = pygame.font.SysFont("monospace", 80, bold = True)
        self.label = self.font.render(text, 0, self.color )
        self.draw()

    #Label zeichnen
    def draw(self):
        self.screen.blit(self.label, (self.posX - self.label.get_rect().width // 2, self.posY))



class Button:
    def __init__(self, color, posX, posY, width, height, text='', size = 25):
        self.color = color
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.text = text
        self.size = size
        self.screen = screen
        self.state = "unvisible"

    #Draw button
    def draw(self, screen, outline=None):
        #Wenn Outline größeres Rechteck mit anderer Farbe unten drunter
        if outline:
            pygame.draw.rect(screen, outline, (self.posX - 2, self.posY - 2, self.width + 4, self.height + 4), 0)

        #Rechteck zeichnen
        pygame.draw.rect(screen, self.color, (self.posX, self.posY, self.width, self.height), 0)

        #Wenn Text nicht leer ist
        if self.text != '':
            font = pygame.font.SysFont('monospace', self.size, bold = True)
            text = font.render(self.text, 1, (0, 0, 0))
            screen.blit(text, (
            self.posX + (self.width / 2 - text.get_width() / 2), self.posY + (self.height / 2 - text.get_height() / 2)))

    #Checken ob Maus über Button, wenn ja return True
    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.posX and pos[0] < self.posX + self.width:
            if pos[1] > self.posY and pos[1] < self.posY + self.height:
                return True

        return False

#Functions
def paint_back():
    screen.fill(bg_color)

#Variablen
counter = 0
playing = False


#Objects
bird = Bird(screen, 230, light_grey, 15)
pipes = [Pipes(screen, light_grey,random.randint(100, 600), random.randint(250, 350), 1025), Pipes(screen, light_grey,random.randint(100, 600), random.randint(250, 350), 900)]
collision = CollisionManager()
score1 = Score(screen, "0", 50, 15, light_grey)
score1copy = Score(screen, "0", 250, 100, light_grey)
highscore = Score(screen, "0", 250, 280,light_grey)
ausgabeh = Textausagbe(screen, 250, 200, light_grey,"Highscore")
ausgabes = Textausagbe(screen, 250, 30, light_grey, "Score")
playbutton = Button(light_grey, 200, 400, 100, 50, "Play")


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
                pipes = [Pipes(screen, light_grey, random.randint(100, 600), random.randint(250, 350), 1025),
                         Pipes(screen, light_grey, random.randint(100, 600), random.randint(250, 350), 900)]
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
        playbutton.state = "unvisible"
        #Schwarzer Hintergrund
        paint_back()
        #Score drawen
        score1.draw()
        #Bird update und draw
        bird.update()
        bird.draw()
        #Ausgewählte Pipe drawen und moven
        pipes[counter].move()
        pipes[counter].draw()
        #Wenn collision bird und pipe playing = False
        if collision.bird_pipes(pipes[counter], bird):
            playing = False
        #Wenn collision bird und floor collision = False
        if collision.bird_floors(bird):
            playing = False
        #Wenn pipe an Bird vorbei ohne Collision increase Score by one
        if collision.points(bird, pipes[counter]):
            score1.increase()
            "Increase"

        #Wenn eine Pipe aus dem Bild raus ist
        if pipes[counter].state == "out":
            #Zwei neue mit random Werten appenden
            pipes.append(Pipes(screen, light_grey, random.randint(100, 600), random.randint(250, 350), 900))
            pipes.append(Pipes(screen, light_grey, random.randint(100, 600), random.randint(250, 350), 900))
            #Wenn der Counter 1 ist setze ihn wieder auf 0 und lösche  beide bereits gefahrenen Pipes aus der Liste
            if counter == 1:
                counter = 0
                del pipes[0:2]
            #Wenn noch nicht 1 Counter einfach erhöhen
            else:
                counter += 1

    #Wenn playing = False
    if playing == False:
        playbutton.state = "visible"
        #Wenn Score höher wie bisheriger Highscore setze neuen Highscore
        if score1.points > highscore.points:
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

    #Display updaten
    pygame.display.update()