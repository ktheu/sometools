# -*- coding: utf-8 -*-

def zeige_unicode_zeichen(z):
    import os
    z = int(z,16)   # umwandlung eines hex-strings in eine int
    html1 = '''
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <style type="text/css">
      body {  color: #555753;
              margin-top: 100px;
              margin-left: 200px;
              font-family: Verdana, Arial, sans-serif;
              font-size: 500%;  }
      </style>
      <title>Unicode</title>
    </head>
    <body>
    <p> '''

    html2 = '''  </p>
    </body>
    </html>
    '''

    ausgabe = [html1,chr(z),html2]
    outfile = 'zeige_unicode_zeichen.html'
    with open(outfile,'w',encoding='utf8') as f:
       f.writelines([x+'\n' for x in ausgabe] )
    os.startfile(outfile)


def zeige_unicode_zeichen_ui():
    s = input('Hexadezimalen Unicode CodePoint: ')
    zeige_unicode_zeichen(s)
