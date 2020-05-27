import sys
from PIL import Image

img = Image.open('cave.jpg')
rgb_im = img.convert('RGB')

width = rgb_im.size[0]
height = rgb_im.size[1]

nimg1 = Image.new( 'RGB', (1000,1000), "white")
nimg2 = Image.new( 'RGB', (1000,1000), "white")

pixels1 = nimg1.load()
pixels2 = nimg2.load()

for i in range(0, width):
    for j in range(0, height):
        if (i + j) % 2 != 0:
            pixels1[i, j] = rgb_im.getpixel((i, j))
        else:
            pixels2[i, j] = rgb_im.getpixel((i, j))

nimg1.save('odd.jpg')
nimg2.save('even.jpg')
