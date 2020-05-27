from PIL import Image, ImageSequence

white_gif = Image.open("white.gif")

positions = open("22_frame_8_positions.txt", "wb")

c = 1
for frame in ImageSequence.Iterator(white_gif):
    frame.save("22_white_frame_%d.gif" % index)
    
    i = list(frame.getdata()).index(8)
    positions.write(str(c) + ": [" + str(i) + "]\n")    

    frame_as_list = open("22_frame_as_list_%d.txt" % c, "wb")
    data = ", ".join(str(v) for v in list(frame.getdata()))
    frame_as_list.write(data)
    frame_as_list.close()
    
    c = c + 1

positions.close()

print "Done :)"
