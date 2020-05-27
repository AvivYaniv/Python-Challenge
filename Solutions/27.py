import Image

zigzag = Image.open('zigzag.gif')
palette = zigzag.getpalette()
palette_table = palette[::3]        # Getting third items, as R=G=B
zigzag_table  = zigzag.getdata()

bzip_bytes = []
diffrence_indexes = []

# between the tabels in zigzag (from one table to other)
for i in range(len(zigzag_table) - 1):     
    if palette_table[zigzag_table[i]] != zigzag_table[i+1]:
        diffrence_indexes.append(i)
        bzip_bytes.append(chr(zigzag_table[i+1]))

s = zigzag.size[0]
clue = Image.new("RGB", zigzag.size, "white")
pixels = clue.load()
for i in diffrence_indexes:
    pixels[i % s, i / s] = (0,) * 3
clue.save("clue.bmp")

import bz2

zigzag_bz = open("zigzag.bz2", 'wb')
zigzag_bz.write(bytearray(bzip_bytes))
zigzag_bz.close()

zigzag_duplicate_words = str.split(bz2.decompress("".join(bzip_bytes)))

import keyword
import difflib

d = difflib.Differ()
# list(set()) to remove duplicates
zigzag_words = list(set(zigzag_duplicate_words))
# the order matters
zigzag_words.sort()
diff = d.compare(zigzag_words, keyword.kwlist)

print "Url, username, and password for level 28: "
print "\n".join(filter(lambda l: l[0] == "-", diff))

print "Done Level 27! :)"
