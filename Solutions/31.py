import Image

def MandelbrotSequenceLength(c, iterations):
    z = complex(0, 0)
    for i in range(iterations):
        z = z * z + c
        if abs(z) > 2:
            return i
    return i

def MandelbrotFractal(left, bottom, width, height, iterations, size):
    regenerated = []
    size_w, size_h = size
    for h in range(size_h)[::-1]:
        for w in range(size_w):
            a = left + w * (width / size_w)
            b = bottom + h * (height / size_h)
            c = complex(a, b)          
            regenerated.append(MandelbrotSequenceLength(c, iterations))
    return regenerated

mandelbrot = Image.open("mandelbrot.gif")
original = mandelbrot.getdata()

size = mandelbrot.size
left=0.34
bottom=0.57     # Denoted as "top", but it's actually bottom
width=0.036
height=0.027
iterations=128

fractal = MandelbrotFractal(left, bottom, width, height, iterations, size)

regenerated = Image.new("L", size)
regenerated.putdata(fractal)
regenerated.save("regenerated.png")

UFOs = []
for i in range(len(original)):
    if original[i] != fractal[i]:
        UFOs.append(original[i] - fractal[i])

# Prime factors of number len(UFOs)=1679 are: 23, 73
arecibo = Image.new("RGB", (23, 73))
arecibo.putdata(UFOs)
arecibo.save("arecibo.png")

print "Done Level 31 :)"
