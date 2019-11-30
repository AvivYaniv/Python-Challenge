import sys
from PIL import Image

img = Image.open('oxygen.png')
rgb_im = img.convert('RGB')

for i in range(0, 87):
    r, g, b = rgb_im.getpixel((i * 7, 45))
    print chr(r),

print "Next level is: "

next_level = [105, 110, 116, 101, 103, 114, 105, 116, 121]
for n in next_level:
    print chr(n), 
