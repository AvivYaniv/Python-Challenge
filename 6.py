import re
import zipfile

z = zipfile.ZipFile("channel.zip", "r")

pathBase = './channel/'
currentNothing = '90052'
for i in range (0, 909):
    currentNotingFileName = currentNothing + '.txt'
    with open(pathBase + currentNotingFileName, 'r') as nothing_file:
        content = nothing_file.read()
        # print content
    parsed = re.split('Next nothing is ', content)
    if len(parsed) <> 2:
        print '\n' + content
    else:        
        print z.getinfo(currentNotingFileName).comment, 
        nextNothing = parsed[1]        
        currentNothing = nextNothing
    
