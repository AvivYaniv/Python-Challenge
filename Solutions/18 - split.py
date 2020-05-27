import re
import codecs

with open('delta.txt') as f:
    lines = f.readlines()

first_png = ''
second_png = ''

nl = len(lines)

for i in range(0, nl):
    l = lines[i]           
    first_png += l[:53] + '\n'      
    second_png += l[56:] 

def hexFromString(s):
    return codecs.getdecoder('hex')(re.sub('[^0-9a-fA-F]', '', s))[0]

with open("first_18.png", 'wb') as f1:
    f1.write(bytearray(hexFromString(first_png)))
    
with open("second_18.png", 'wb') as f2:
    f2.write(bytearray(hexFromString(second_png)))

print "Done :)"
