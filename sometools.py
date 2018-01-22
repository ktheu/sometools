'''
Eine neue Auswahl in die Liste eingaben aufnehmen.
Eine Abkürzung in Klammern dahinter schreiben. - 
'''

eingaben = ['collatz(col)','ggt','binhextest(bht)','addnum(adn)','subnum(sbn)']

def help_():
    print('Verfügbare Kommandos (Abkürzung in Klammern):')
    print(*eingaben)

edict = {}   # dictionary mit den gültigen Eingaben
for x in eingaben:
    p1 = x.find('(')
    if p1 > 0:
        p2 = x.find(')')
        abk = x[p1+1:p2]  # abkürzung
        cmd = x[:p1]      # kommando
        edict[cmd] = cmd
        edict[abk] = cmd
    else:
        edict[x] = x

print('Eingabe oder q(quit), h(help)')
while True:
    print('-> ',end='')
    eingabe = input()
    if eingabe == 'q':
        print('Goodbye')
        break
    elif eingabe == 'h':
        help_()
    elif eingabe not in edict:
        print('Ungültige Eingabe')
    else:
        exec('from ' + edict[eingabe] + ' import *')
        exec(edict[eingabe]+'_ui()')
