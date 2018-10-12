############################################################
# IMPORTS
############################################################
import pygame


############################################################
# FUNKTIONEN
############################################################
def BaumDarstellen(baum):
    b = baum
    layer = -1
    while not b.empty():
        b = b.left()
        layer += 1
    drawBaum(baum, 30, layer)
    end = False
    while not end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                end = True


def drawBaum(baum, sgroeße, layer):
    pygame.init()
    font = pygame.font.SysFont('Arial', sgroeße)
    screen = pygame.display.set_mode([(2 ** layer) * sgroeße * 2 + sgroeße, layer * 2 * sgroeße + 3 * sgroeße])
    screen.fill([255, 255, 255])
    recursiveDraw(screen, font, baum, [2 ** layer * sgroeße, sgroeße], sgroeße, layer, 0)
    pygame.display.flip()


def recursiveDraw(screen, font, baum, pos, sgroeße, maxlayer, layer):
    if baum.empty(): return False
    num = str(baum.value())
    numrender = font.render(num, False, [0, 0, 0])
    x = pos[0]
    y = pos[1]
    newX1 = x + sgroeße * 2 ** (maxlayer - (layer + 1))
    newX2 = x - sgroeße * 2 ** (maxlayer - (layer + 1))
    newY = y + 2 * sgroeße
    newpos1 = [newX1, newY]
    newpos2 = [newX2, newY]
    if len(num) == 2:
        screen.blit(numrender, pos)

    elif len(num) == 1:
        # x += sgroeße/2
        screen.blit(numrender, [x + sgroeße / 4, y])
        x += sgroeße / 4
    num1 = recursiveDraw(screen, font, baum.left(), newpos2, sgroeße, maxlayer, layer + 1)
    if num1 == 2:
        pygame.draw.line(screen, [0, 0, 0], [x, y + sgroeße], [newX2 + sgroeße / 2, newY])
    elif num1 == 1:
        pygame.draw.line(screen, [0, 0, 0], [x, y + sgroeße], [newX2 + sgroeße / 2, newY])
    if len(num) == 2:
        x += sgroeße / 2
    if recursiveDraw(screen, font, baum.right(), newpos1, sgroeße, maxlayer, layer + 1):
        pygame.draw.line(screen, [0, 0, 0], [x + sgroeße / 2, y + sgroeße], [newX1 + sgroeße / 2, newY])
    return len(num)


############################################################
# KLASSEN
############################################################
class Knoten:
    def __init__(self, x=None):
        self.inhalt = x
        self.links = None
        self.rechts = None

    def __str__(self):
        return self.inhalt.__str__()


class Baum:
    def __init__(self, x=None, l=None, r=None):
        self.wurzel = None
        if x is not None:
            self.wurzel = Knoten(x)
        if l is not None:
            self.wurzel.links = l.wurzel
        if r is not None:
            self.wurzel.rechts = r.wurzel

    def empty(self):
        return self.wurzel is None

    def value(self):
        if self.empty(): raise RuntimeError("Fehler: Baum ist leer")
        return self.wurzel.inhalt

    def left(self):
        if self.empty(): raise RuntimeError("Fehler: Baum ist leer")
        temp = Baum()
        temp.wurzel = self.wurzel.links
        return temp

    def right(self):
        if self.empty(): raise RuntimeError("Fehler: Baum ist leer")
        temp = Baum()
        temp.wurzel = self.wurzel.rechts
        return temp

    def __str__(self):
        if self.empty(): return ""
        s = self.baumString(0)
        if len(s) > 0:
            s = s[:-1]
        return s

    def baumString(self, tiefe):
        s = ""
        punkte = "." * tiefe
        if not self.right().empty():
            s = s + self.right().baumString(tiefe + 1)
        if self.value() is None:
            s = s + punkte + "leer\n"
        else:
            s = s + punkte + str(self.value().__str__()) + "\n"
        if not self.left().empty():
            s = s + self.left().baumString(tiefe + 1)
        return s
