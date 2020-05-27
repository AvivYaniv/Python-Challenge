import string
from string import maketrans

def RorByDiff(diff, encrypted):
    abc = string.ascii_lowercase
    abc_enc = ""

    n = len(abc)
    for i in range (0, len(string.ascii_lowercase)):
        abc_enc += chr(ord('a') + (i + diff) % n)

    rot = maketrans(abc, abc_enc)

    print "Translated ROT" + str(diff) + ": "
    decrypted = encrypted.translate(rot)
    print decrypted

# Translated ROT13: in the face of what
# print 'va gur snpr bs jung?'.decode('rot13')
for i in range(24):
    RorByDiff(i, "va gur snpr bs jung")
