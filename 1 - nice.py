import string
from string import maketrans

print 'K->M, diffrence: ' + str(ord('M')-ord('K'))
print 'Q->O, diffrence: ' + str(ord('Q')-ord('O'))
print 'G->E, diffrence: ' + str(ord('G')-ord('E'))

diff = ord('M')-ord('K')

abc = string.ascii_lowercase
abc_enc = abc[diff:]+abc[:diff]

ceasar = maketrans(abc, abc_enc)

encrypted = raw_input("Enter Ceaser encrypted Please  : ")

print "Translated Ceasar " + str(diff) + " places identation: "
decrypted = encrypted.translate(ceasar)
print decrypted
