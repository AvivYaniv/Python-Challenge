import sys
from PIL import Image

nimg = Image.new( 'RGB', (1000,1000), "white")
rgb_im = nimg.convert('RGB')
pixels = nimg.load()

bytes_read = open("evil2.gfx", "rb").read()

for c in range(0, 6):
    n = c
    file_b = open("extract_evil_" + str(n + 1) + ".png", "wb")    

    while (n + 10) < len(bytes_read):
        r2, g2, b2 = ord(bytes_read[n]), ord(bytes_read[n + 5]), ord(bytes_read[n + 10])
        n = n + 15

        file_b.write(chr(r2))
        file_b.write(chr(g2))
        file_b.write(chr(b2))

    file_b.close()
