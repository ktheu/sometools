############################################################
# IMPORTS
############################################################
import pygame
import random


############################################################
# FUNKTIONEN
############################################################
def BaumDarstellen(baum):
    layer = findeTiefe(baum) - 1
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


def findeTiefe(baum):
    '''
    Gibt die Toefe des Bauems zurück gezählt ab 1
    :param baum: Baum
    :return: int
    '''
    if baum.empty(): return 0
    return max(findeTiefe(baum.left()), findeTiefe(baum.right())) + 1


def anzahlKnoten(baum):
    '''
    zählt wie viele Knoten ein Baum hat
    :param baum: Baum
    :return: int
    '''
    if baum.empty(): return 0
    return anzahlKnoten(baum.left()) + anzahlKnoten(baum.right()) + 1


def randomBaum(tiefe=None, minKnoten=None):
    '''
    kreiert ein random Baum
    :param tiefe: int
    :param minKnoten: int, nicht kleiner als 2**tiefe-1
    :return: Baum
    '''
    if tiefe is None:
        tiefe = 4
    if minKnoten is None:
        minKnoten = 2 ** (tiefe - 1)
    baume = []
    for i in range(random.randint(2 ** (tiefe - 1), 2 ** tiefe)):
        baume.append(Baum(random.randint(1, 30)))
    while len(baume) > 1:
        n = random.random()
        if n > 0.9:
            n = random.randint(1, 2)
            elem = random.choice(baume)
            baume.remove(elem)
            if n == 1:
                baume.append(Baum(random.randint(1, 30), elem, None))
                if findeTiefe(baume[-1]) == tiefe: return baume[-1]
            else:
                baume.append(Baum(random.randint(1, 30), None, elem))
                if findeTiefe(baume[-1]) == tiefe: return baume[-1]
        else:
            elem1 = random.choice(baume)
            baume.remove(elem1)
            elem2 = random.choice(baume)
            baume.remove(elem2)
            baume.append(Baum(random.randint(1, 30), elem1, elem2))
            if findeTiefe(baume[-1]) == tiefe:
                if anzahlKnoten(baume[-1]) >= minKnoten:
                    return baume[-1]
                else:
                    return randomBaum(tiefe, minKnoten)
    if anzahlKnoten(baume[0]) >= minKnoten:
        return baume[0]
    else:
        return randomBaum(tiefe, minKnoten)


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
