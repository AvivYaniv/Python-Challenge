import Image

# Open the yankeedoodle CSV file
yankeedoodle_file = open("yankeedoodle.csv")

# Removing delimeters (space & new-line) and splitting floats
yankeedoodle_floats = yankeedoodle_file.read().translate(None, ' \n').split(',')

# Prime factors of number len(yankeedoodle_floats)=7367 are: 53, 139
im = Image.new("L", (53, 139))
im.putdata(bytearray([int(float(f) * 256) for f in yankeedoodle_floats]))
im = im.rotate(270).transpose(Image.FLIP_LEFT_RIGHT)
im.save('equation.png')


message = []
x=yankeedoodle_floats
# Given the equation:
# n=str(x[i])[5]+str(x[i+1])[5]+str(x[i+2])[6]
for i in range(0, len(yankeedoodle_floats)-3, 3):
    n=str(x[i])[5]+str(x[i+1])[5]+str(x[i+2])[6]    
    message.append(chr(int(n)))

print "".join(message)
