import re
import codecs

with open('delta.txt') as f:
    lines = f.readlines()

first_png = ''
second_png = ''

nl = len(lines)

half_line_length = len(lines[0]) / 2
first_index = half_line_length - 2
second_index = half_line_length + 1 

for i in range(0, nl):
    l = lines[i]           
    first_png += l[:first_index] + '\n'      
    second_png += l[second_index:] 

# Decode Hex to string
# e.g. "0a" -> "\n"
def hexFromString(s):
    # Removing non-hex resambling stings
    cleared_string = re.sub('[^0-9a-fA-F]', '', s)
    # Getting Hex decoder
    hex_decoder = codecs.getdecoder('hex')
    return hex_decoder(cleared_string)[0]

with open("first_18.png", 'wb') as f1:
    f1.write(bytearray(hexFromString(first_png)))
    
with open("second_18.png", 'wb') as f2:
    f2.write(bytearray(hexFromString(second_png)))

import difflib

lines_diffrences = list(difflib.Differ().compare(
         first_png.splitlines(),
         second_png.splitlines()))

both_png = open("18_both.png", 'wb')
only_first_png = open("18_only_first.png", 'wb')
only_second_png = open("18_only_second.png", 'wb')

for lndf in lines_diffrences:
    lc = lndf[2:]
    if lndf[0] == " ":
        both_png.write(hexFromString(lc))
    elif lndf[0] == "-":        
        only_first_png.write(hexFromString(lc))
    elif lndf[0] == "+":
        only_second_png.write(hexFromString(lc))

print "Done :)"
