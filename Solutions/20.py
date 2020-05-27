import httplib, base64

headers = {"Authorization": "Basic " + base64.b64encode('butter:fly')}
con = httplib.HTTPConnection("www.pythonchallenge.com")

path = "/pc/hex/unreal.jpg"

def GetByRange(start, end):
    range = "bytes=%s-%s" % (start, end)
    headers["Range"] = range
    
    print range
    
    con.request("GET", path, "", headers)    

    try:
        response = con.getresponse().read()
    
    except httplib.BadStatusLine:
        pass

    if response:        
        print response

        unreal_txt = open("20_unreal_%s.txt" % range, 'wb')
        unreal_txt.write(response)
        unreal_txt.close()
        
        return len(response)

    return 10

##x = 30203
##r = 0
##for i in range(0, 500):
##    r = GetByRange(x, x + r)
##    x += r

##x = 2117297010
##x = 2117298783
##x = 2117298941
##x = 2117301920
##x = 2117303647
##x = 2117306983
##x = 2117309434
##x = 2117313587
##x = 2123453587
##r = 10
##while x <= 2123456789:
##    r = GetByRange(x, x + r)
##    x += r

x = 1152983631
r = 10
while x <= 2123456789:
    r = GetByRange(x, x + r)
    x += r
    
print "Done :)"
