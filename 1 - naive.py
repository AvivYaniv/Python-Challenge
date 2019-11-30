import string

print 'K->M, diffrence: ' + str(ord('M')-ord('K'))
print 'Q->O, diffrence: ' + str(ord('Q')-ord('O'))
print 'G->E, diffrence: ' + str(ord('G')-ord('E'))

diff = ord('M')-ord('K')

encrypted = raw_input("Enter Ceaser encrypted Please  : ")
decrypted = ""

for c in encrypted:
    if c.isalpha():
        n = len(string.ascii_lowercase)
        decrypted += string.ascii_lowercase[(ord(c.lower()) + diff - ord('a')) % n]
    else:
        decrypted += c

print "Translated Ceasar " + str(diff) + " places identation: "
print decrypted
