import re
import urllib

urlBegining = 'http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing='

currentNothing = '12345'
#currentNothing = '16044'
for i in range (0, 400):
    openedUrl = urllib.urlopen(urlBegining + currentNothing)
    content = openedUrl.read()
    parsed = re.split('and the next nothing is ', content)
    if len(parsed) == 1:
        print content
        if content != 'Yes. Divide by two and keep going.':
            break
        else:
            currentNothing = str(int(currentNothing) / 2)      
    else:
        nextNothing = parsed[1]
        print content + '=> next nothing is: ' + nextNothing
        currentNothing = nextNothing
        

