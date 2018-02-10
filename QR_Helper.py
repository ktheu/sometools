def QR_Helper_ui():
    print('Dieser QR-Code Helper kann NUR für 21*21 QR-Codes weitegehend Helfen(Mask, Mode und ICC gehen mit jedem QR-Code)')
    form = input('Format?')
    try:
        decoded_form = form_decode()[form]
    except:
        print('Fehlerhaftes Format!')
        return
    print(decoded_form)
    fehlerkorrekt = decoded_form[17]
    mask = int(decoded_form[-2])
    maskList = crateMaskList(mask)
    temp = input('Maske Printen? j/n')
    if temp == 'j':
        for i in range(0,len(maskList)):
            for j in range(0,len(maskList[i])):
                print(maskList[j][i], end=' ')
            print()
    maskList_1D = create1dMask(maskList)
    pos_maskList_1D = 0
    mode = input('Mode? ')
    print('Mask: ' + ''.join(maskList_1D[:4]))
    pos_maskList_1D += 4
    decoded_mode = decode(mode, maskList_1D[:4])
    str_mode, cci_str, cci_len, data_len, data_inf, end = setModeConstans(decoded_mode)
    print('Decoded Mode: ' + decoded_mode)
    print('Also ' + str_mode)
    if cci_str == None: return      # Break if Kanji
    print(cci_str)
    cci = input('CCI?')
    print('Mask: ' + ''.join(maskList_1D[pos_maskList_1D:cci_len+pos_maskList_1D]))
    decoded_cci = decode(cci, maskList_1D[pos_maskList_1D:cci_len+pos_maskList_1D])
    pos_maskList_1D += cci_len
    print('Decoded CCI: ' + decoded_cci)
    print('Also:', binaerDecimal(decoded_cci),'Stellen')
    print('Dies sind', round((binaerDecimal(decoded_cci)/data_inf)+0.5),'Blöcke')
    print('Blöcke haben', data_len, 'Bits')
    print('Der Letzte Block hat', end[binaerDecimal(decoded_cci) % data_inf], 'Bits')
    parts = round((binaerDecimal(decoded_cci)/data_inf)+0.5)
    last_part = end[binaerDecimal(decoded_cci) % data_inf]
    information = ''
    for i in range(0, parts):
        if i == parts-1:
            daten = input('Daten?(' + str(last_part) + ' lang)')
            print('Mask:', ''.join(maskList_1D[pos_maskList_1D:last_part+pos_maskList_1D]))
            raw_data = decode(daten, maskList_1D[pos_maskList_1D:last_part+pos_maskList_1D])
            pos_maskList_1D += last_part
        else:
            daten = input('Daten?(' + str(data_len) + ' lang)')
            print('Mask:', ''.join(maskList_1D[pos_maskList_1D:data_len+pos_maskList_1D]))
            raw_data = decode(daten, maskList_1D[pos_maskList_1D:data_len+pos_maskList_1D])
            pos_maskList_1D += data_len
        print('Raw:', raw_data)
        information += str(charDecode(raw_data, str_mode))
        print('Bisher encoded:', information)
    print('Fertig encoded:', information)

def charDecode(s, type):
    keys = list(range(45))
    values = list(range(10))
    for i in range(ord('A'), ord('Z')+1):
        values.append(chr(i))
    values += [' ', '$', '%', '*','+','-','.','/',':']
    alphanumeric = dict(zip(keys,values))
    num = binaerDecimal(s)
    if type == 'Byte':
        return chr(num)
    elif type == 'Numeric':
        num = str(num)
        if len(s) == 10:
            while len(num) < 3:
                num = '0' + num
            return num
        elif len(s) == 7:
            while len(num) < 2:
                num = '0' + num
            return num
        else:
            while len(num) < 1:
                num = '0' + num
            return num
    else:
        if len(s) == 6:
            return alphanumeric[num]
        else:
            return str(alphanumeric[num//45]) + str(alphanumeric[num%45])


def binaerDecimal(s):
    num = 0
    for i in range(0, len(s)):
        num += int(s[-(i+1)])*2**i
    return num
def setModeConstans(mode):
    if mode == '0001':
        str_mode = 'Numeric'
        cci_str = 'CCI: 10 Bit\n3 Ziffern 10 Bit\nEin Zeichen 4 Bit\nZwei Zeichen 7 Bit'
        cci_len = 10
        data_len = 10
        data_inf = 3
        end = {1: 4, 2: 7, 0:10}
    elif mode == '0010':
        str_mode = 'Alphanumeric'
        cci_str = 'CCI: 9 Bit\nZwei Zeichen 11 Bit\nFür ein Zeichen 6 Bit'
        cci_len = 9
        data_len = 11
        data_inf = 2
        end = {1: 6, 0:11}
    elif mode == '0100':
        str_mode = 'Byte'
        cci_str = 'CCI: 8 Bit\nJedes Zeichen 8 Bit'
        cci_len = 8
        data_len = 8
        data_inf = 1
        end = {0:8}
    else:
        str_mode = 'Kanji (Kann nicht Helfen)'
        cci_str = None
        cci_len = None
        data_len = None
        data_inf = None
        end = None
    return str_mode, cci_str, cci_len, data_len, data_inf, end

def form_decode():
    form_dict = {'111011111000100': 'Fehlerkorrektur: L\nMaske: 000 (0)',
                 '111001011110011': 'Fehlerkorrektur: L\nMaske: 001 (1)',
                 '111110110101010': 'Fehlerkorrektur: L\nMaske: 010 (2)',
                 '111100010011101': 'Fehlerkorrektur: L\nMaske: 011 (3)',
                 '110011000101111': 'Fehlerkorrektur: L\nMaske: 100 (4)',
                 '110001100011000': 'Fehlerkorrektur: L\nMaske: 101 (5)',
                 '110110001000001': 'Fehlerkorrektur: L\nMaske: 110 (6)',
                 '110100101110110': 'Fehlerkorrektur: L\nMaske: 111 (7)',
                 '101010000010010': 'Fehlerkorrektur: M\nMaske: 000 (0)',
                 '101000100100101': 'Fehlerkorrektur: M\nMaske: 001 (1)',
                 '101111001111100': 'Fehlerkorrektur: M\nMaske: 010 (2)',
                 '101101101001011': 'Fehlerkorrektur: M\nMaske: 011 (3)',
                 '100010111111001': 'Fehlerkorrektur: M\nMaske: 100 (4)',
                 '100000011001110': 'Fehlerkorrektur: M\nMaske: 101 (5)',
                 '100111110010111': 'Fehlerkorrektur: M\nMaske: 110 (6)',
                 '100101010100000': 'Fehlerkorrektur: M\nMaske: 111 (7)',
                 '011010101011111': 'Fehlerkorrektur: Q\nMaske: 000 (0)',
                 '011000001101000': 'Fehlerkorrektur: Q\nMaske: 001 (1)',
                 '011111100110001': 'Fehlerkorrektur: Q\nMaske: 010 (2)',
                 '011101000000110': 'Fehlerkorrektur: Q\nMaske: 011 (3)',
                 '010010010110100': 'Fehlerkorrektur: Q\nMaske: 100 (4)',
                 '010000110000011': 'Fehlerkorrektur: Q\nMaske: 101 (5)',
                 '010111011011010': 'Fehlerkorrektur: Q\nMaske: 110 (6)',
                 '010101111101101': 'Fehlerkorrektur: Q\nMaske: 111 (7)',
                 '001011010001001': 'Fehlerkorrektur: H\nMaske: 000 (0)',
                 '001001110111110': 'Fehlerkorrektur: H\nMaske: 001 (1)',
                 '001110011100111': 'Fehlerkorrektur: H\nMaske: 010 (2)',
                 '001100111010000': 'Fehlerkorrektur: H\nMaske: 011 (3)',
                 '000011101100010': 'Fehlerkorrektur: H\nMaske: 100 (4)',
                 '000001001010101': 'Fehlerkorrektur: H\nMaske: 101 (5)',
                 '000110100001100': 'Fehlerkorrektur: H\nMaske: 110 (6)',
                 '000100000111011': 'Fehlerkorrektur: H\nMaske: 111 (7)'}
    return form_dict

def crateMaskList(maskNum):
    allMaskList = ['(i+j)%2==0', 'j%2==0', 'i%3==0', '(i+j)%3==0',
                   '(j//2+i//3)%2==0', '(i*j)%2+(i*j)%3==0',
                   '((i*j)%2+(i*j)%3)%2==0', '((i*j)%3+(i+j)%2)%2==0']
    maskList = []
    for i in range(0, 21):
        tempList = []
        for j in range(0, 21):
            if eval(allMaskList[maskNum]):
                tempList.append('X')
            else:
                tempList.append('-')
        maskList.append(tempList)
    return maskList
def decode(data, mask):
    string = ''
    for i in range(0, len(data)):
        if data[i] == mask[i]:
            string += '0'
        else:
            string += '1'
    return string
def create1dMask(l):
    list = []
    for j in range(0,2):
        for i in range(0, 12):
            list.append(l[20-4*j][20-i])
            list.append(l[19-4*j][20-i])
        for i in range(11, -1, -1):
            list.append(l[18-4*j][20-i])
            list.append(l[17-4*j][20-i])
    for i in range(0, 14):
        list.append(l[12][20-i])
        list.append(l[11][20-i])
    for i in range(0, 6):
        list.append(l[12][5-i])
        list.append(l[11][5-i])
    for i in range(5, -1, -1):
        list.append(l[12][5 - i])
        list.append(l[11][5 - i])
    for i in range(13, -1, -1):
        list.append(l[12][20-i])
        list.append(l[11][20-i])
    for i in range(0, 4):
        list.append(l[8][12-i])
        list.append(l[7][12-i])
    for i in range(-3, -1, -1):
        list.append(l[5][12-i])
        list.append(l[4][12-i])
    for i in range(0,4):
        list.append(l[3][12-i])
        list.append(l[2][12-i])
    for i in range(-3, -1, -1):
        list.append(l[1][12 - i])
        list.append(l[0][12 - i])
    return [c.replace('X','1').replace('-','0')for c in list]