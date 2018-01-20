def collatz(x):
    '''
    x: positive ganze Zahl
    returns: Collatz-Zahl für x
    '''
    zaehl = 0
    while x != 1:
        if x % 2 == 0:
            x = x // 2
        else:
            x = 3*x+1
        zaehl+=1
    return zaehl


def collatz_ui():
    n = int(input('Bitte eine positive ganze Zahl eingeben: '))
    print('Die Collatz-Zahl für',n,'ist',collatz(n))
