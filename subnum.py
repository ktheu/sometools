"""
Created on Mon Jan 22 08:47:14 2018

@author: ktheu
"""

def subnum(a,b):
    return a-b

def subnum_ui():
    eingabe = input('Bitte zwei Zahlen eingeben: ')
    x, y = [int(x) for x in eingabe.split()]
    print('Die Differenz ist',subnum(x,y))
    
if __name__ == '__main__':
    subnum_ui()
