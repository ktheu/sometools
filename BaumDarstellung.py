############################################################
# IMPORTS
############################################################
import pygame


############################################################
# FUNKTIONEN
############################################################
def createBaum(baumliste, layer=0):
    if len(baumliste) == 1:
        return Baum(baumliste[0][layer:])
    elif len(baumliste) == 0:
        return None
    for i in range(0, len(baumliste)):
        if baumliste[i][layer:].isnumeric():
            index = i
            elem = baumliste[i][layer:]
    return Baum(elem, createBaum(baumliste[index + 1:], layer=layer + 1),
                createBaum(baumliste[:index], layer=layer + 1))


def drawBaum(baum, sgroeße, layer, screenshot, dateiname):
    pygame.init()
    font = pygame.font.SysFont('Arial', sgroeße)
    screen = pygame.display.set_mode([(2 ** layer) * sgroeße * 2 + sgroeße, layer * 2 * sgroeße + 3 * sgroeße])
    screen.fill([255, 255, 255])
    recursiveDraw(screen, font, baum, [2 ** layer * sgroeße, sgroeße], sgroeße, layer, 0)
    pygame.display.flip()
    if screenshot:
        pygame.image.save(screen, dateiname)


def recursiveDraw(screen, font, baum, pos, sgroeße, maxlayer, layer):
    if baum.empty(): return False
    num = baum.value()
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


def BaumDarstellung_ui():
    cmd = input('Wollen sie aus einem File lesen (f) oder den Baum von Hand eingeben (h)?')
    if cmd.lower() == 'f':
        dateiname = input('Dateiname:\n')
        file = open(dateiname, 'r')
        baumList = file.readlines()
        for i in range(0, len(baumList)):
            if baumList[i][-1] == '\n':
                baumList[i] = baumList[i][:-1]
            elif baumList[i] == '':
                del baumList[i]

    elif cmd.lower() == 'h':
        print('Geben Sie den Baum zeile pro zeile an')
        eingabe = input()
        baumList = []
        while eingabe != '':
            baumList.append(eingabe)
            eingabe = input()
    else:
        print('Ungültige Eingabe')
        return
    schrift = input('Schriftgröße?')
    if schrift == '':
        schrift = 30
    else:
        schrift = int(schrift)
    baum = createBaum(baumList)
    layerList = [i.count('.') for i in baumList]
    layer = max(layerList)
    dateiname = input(
        'Dateiname zum speichern des Bildes: Wenn kein Dateiname angegeben wird wird das bild nicht gescpeichert')
    if dateiname == '':
        screenshot = False
    else:
        screenshot = True
        try:
            if dateiname[-4:] != '.jpg':
                dateiname += '.jpg'
        except:
            dateiname += '.jpg'
    drawBaum(baum, schrift, layer, screenshot, dateiname)
    end = False
    while not end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                end = True


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


############################################################
# MAIN
############################################################
if __name__ == '__main__':
    BaumDarstellung_ui()
