import Image

def whodunnit():
    return "Guido van Rossum".lower()

bell = Image.open("bell.png")
bell = bell.convert("RGB")

message = []
green = bell.split()[1].getdata()
for i in range(0, len(green) - 1, 2):
    d = abs(green[i+1]-green[i])
    if d != 42:
        message.append(chr(d))

print "".join(message)
print whodunnit().split()[0]
