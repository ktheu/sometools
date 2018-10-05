def ggt(a,b):
    '''
    a,b: positive ganze Zahlen
    returns: größten gemeinsamen Teiler von a und b
    '''
    while a != b:
        if a > b:
            a = a - b
        else:
            b = b - a
    return a


def ggt_ui():
    print('Der größte gemeinsame Teiler zweier positiver ganzen Zahlen wird berechnet.')
    eingabe = input('Bitte die beiden Zahlen mit blank getrennt eingeben: ')
    x, y = [int(a) for a in eingabe.split()]
    print('Der ggT von',x,'und',y,'ist',ggt(x,y))
