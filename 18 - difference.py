import sys
from PIL import Image

img = Image.open('balloons.jpg')
rgb_im = img.convert('RGBA')

h, w = img.size
halfH = h / 2

nimg = Image.new('RGBA', (375,335), "white")
pixels = nimg.load()

p = 0
s = ''

for i in range(0, halfH):
    for j in range(0, w):        
        r1, g1, b1, a1 = rgb_im.getpixel((i, j))
        r2, g2, b2, a2 = rgb_im.getpixel((i + halfH, j))   

        dr = abs(r1 - r2)
        dg = abs(g1 - g2)
        db = abs(b1 - b2)
        da = abs(a1 - a2)

##        p = p + 1
##        if p <=  2:
##            print p
##            print i, j
##            print i + halfH, j
##            print dr, dg, db
##            print '\n'
        
        pixels[i, j] = (dr, dg, db, da)

nimg.save("difference.jpg")
