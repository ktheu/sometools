"""
Created on Mon Jan 22 08:47:14 2018

@author: ktheu
"""

def addnum(a,b):
    return a+b

def addnum_ui():
    eingabe = input('Bitte zwei Zahlen eingeben: ')
    x, y = [int(x) for x in eingabe.split()]
    print('Die Summe ist',addnum(x,y))
    
if __name__ == '__main__':
    addnum_ui()
