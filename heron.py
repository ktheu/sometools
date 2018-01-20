def heron(a, x, n):
    ''' 
    a, x: floats
    n: positive ganze Zahl
    returns: Liste mit den Näherungen von Wurzel a bei erster Schätzung x 
    nach dem Heron-Verfahren. Die letzte Näherung zum Quadrat und a sind
    in den ersten n Dezimalstellen gleich.
    '''
    temp = []
    e = 10**-(n+1)        # auf n Stellen genau
    while abs(x**2-a) > e:
        temp.append(x)
        x = 0.5 * (x + a/x)
    temp.append(x)
    return temp 