import random
import time

def bin_hex(s):
    if s == '0000': return '0'
    if s == '0001': return '1'
    if s == '0010': return '2'
    if s == '0011': return '3'
    if s == '0100': return '4'
    if s == '0101': return '5'
    if s == '0110': return '6'
    if s == '0111': return '7'
    if s == '1000': return '8'
    if s == '1001': return '9'
    if s == '1010': return 'A'
    if s == '1011': return 'B'
    if s == '1100': return 'C'
    if s == '1101': return 'D'
    if s == '1110': return 'E'
    if s == '1111': return 'F'


def binhextest_ui():
    runden = int(input('Runden?: '))
    start = time.time()
    falsch = 0
    for i in range(0, runden):
        aktuell = str(random.randint(0,1)) + str(random.randint(0,1)) + str(random.randint(0,1)) + str(random.randint(0,1))
        test = input(aktuell + ' ')
        if test.lower() == bin_hex(aktuell).lower():
            print('Richtig')
        else:
            print('Falsch')
            print(bin_hex(aktuell))
            falsch += 1
    print('Du hast: ' + str(round(falsch / runden, 2) * 100) +'% Falsch gemacht.')
    print('Du hast ' + str(round(time.time() - start, 2)) + ' Sekunden gebraucht')

    print('Das sind ' + str(round(round(time.time() - start, 2)/ runden, 2)) + 'Sekunden pro Runde')

if __name__ == '__main__':
    binhextest_ui()
