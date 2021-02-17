import pygame
#Variablen
light_grey = (200,200,200)
class Bird:
    def __init__(self, screen, posX, color, radius):
        self.height = 900
        self.screen = screen
        self.color = color
        self.posX = posX
        self.posY = self.height //2
        self.gravity = 0.002
        self.lift = -0.5
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

        if self.posY >= self.height - self.radius:
            self.posY = self.height - self.radius
            self.velocity = 0

        if self.posY - self.radius <= 0:
            self.posY = 0 + self.radius
            self.velocity = 0
    #Restartet Position von Bird bei playing = False
    def restart(self):
        self.posX = 100 #230
        self.posY = self.height // 2

class Pipes:
    def __init__(self, screen, color, height, gap, posX):
        self.color = color
        self.screen = screen
        self.width = 50
        self.posX = posX
        self.gap = gap
        self.posY = 0
        self.speed = 0.22
        self.height = height
        self.state = "in"

    #Malt obere und untere Hälfte getrennt voneinander aber mit gleichen X Koordinaten
    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.posX, self.posY, self.width, self.height))
        pygame.draw.rect(self.screen, self.color, (self.posX, self.posY + self.height + self.gap, self.width, 900 - self.height - self.gap))

    #Moved pipes über Screen
    def move(self):
        self.posX -= self.speed

        #Wenn Pipe zur Hälfte aus Bild raus ändere Status zu out
        if self.posX < 0 - 50:
            self.state = "out"
            self.speed = 0

    def collide(self, bird):
        if bird.posY - bird.radius <= self.height or bird.posY + bird.radius >= self.height + self.gap:
            if bird.posX - bird.radius >= self.posX and bird.posX + bird.radius <= self.posX + self.width:
                return True

    # Checkt ob Pipe an Bird vorbei ohne Berührung
    def points(self, bird):
        if self.posX + self.width < bird.posX - 15 and self.posX + self.width > bird.posX - 15.1:
            return True

    def append(self):
        if self.posX < 400 and self.posX > 399.9:
            return True


class CollisionManager:

    #Checked ob Bird Floor berührt
    def bird_floors(self, bird):
        if bird.posY + bird.radius > 899 or bird.posY - bird.radius < 1:
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
    def __init__(self, screen, color, posX, posY, width, height, text='', size = 25):
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