import bz2
import urllib

level29 = urllib.urlopen("http://repeat:switch@www.pythonchallenge.com/pc/ring/guido.html")
lines = level29.read().split('\n') 

message = []
for l in lines:
    if not any(c.isalpha() for c in l):
        message.append(chr(len(l)))

# Isn't it clear? I am yankeedoodle!
print bz2.decompress("".join(message)) 
