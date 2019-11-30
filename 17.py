import re
import bz2
import urllib

import xmlrpclib
import urllib2

urlBegining = 'http://www.pythonchallenge.com/pc/def/linkedlist.php?busynothing='

bzMessage = r''

currentNothing = '12345'
for i in range (0, 400):    
    URL=urlBegining + currentNothing

    openedUrl = urllib.urlopen(URL)
    
    raw_cookie=dict(openedUrl.info())['set-cookie']    
    cookie_splitted=re.split(';', raw_cookie)

    cookie_dict={}
    for token in range(len(cookie_splitted)):
        token_split=re.split('=', cookie_splitted[token])
        cookie_dict[token_split[0].strip()]=token_split[1]

##    knownCookies=['info', 'expires', 'path', 'domain']
##    for key, value in cookie_dict.iteritems():
##        if all(key.find(k)<0 for k in knownCookies):
##            print key, ' : ', value

    if cookie_dict['info'] != 'deleted':
        bzMessage = bzMessage + cookie_dict['info']
            
    content = openedUrl.read()
    openedUrl.close()
    
    parsed = re.split('and the next busynothing is ', content)

    if len(parsed) < 2:
        print "Last i: ", i
        break
    else:
        nextNothing = parsed[1]
        ##  print content + '=> next nothing is: ' + nextNothing
        currentNothing = nextNothing

bzMessage = urllib.unquote_plus(bzMessage)
print 'Bz Message (original): \n', bzMessage
# is it the 26th already? call his father and inform him that "the flowers are on their way". he'll understand.
print 'Bz Message (decompressed): \n', bz2.decompress(bzMessage.decode('string_escape'))

proxy = xmlrpclib.ServerProxy("http://www.pythonchallenge.com/pc/phonebook.php")

## is it the 26th already? call his father and inform him that "the flowers are on their way". he'll understand.
## 555-VIOLIN
print str(proxy.phone('Leopold'))

uri = "http://www.pythonchallenge.com/pc/stuff/violin.php"
msg = "the flowers are on their way"
rq = urllib2.Request(uri, headers = { "Cookie": "info=" + urllib.quote_plus(msg)})

print urllib2.urlopen(rq).read()

