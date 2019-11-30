import httplib, base64

headers = {"Authorization": "Basic " + base64.b64encode('butter:fly')}
con = httplib.HTTPConnection("www.pythonchallenge.com")

for i in range(1, 26):
    print i    
    con.request("GET", "/pc/hex/lake%s.wav" % i, "", headers)

    try:
        response = con.getresponse().read()
    
    except httplib.BadStatusLine:
        pass

    if response:
        lake_wav = open("lake%s.wav" % i, 'wb')
        lake_wav.write(response)
        lake_wav.close()

print "Done downloading Lake.Wav's, Level: 25"

import wave
import math
import Image

lake_frames = []
frames_length = 0
puzzle_part_length = 0
for i in range(1, 26):
    lake_wav = wave.open("lake%s.wav" % i, 'rb')

    frames = lake_wav.readframes(lake_wav.getnframes())
    frames_length = frames_length + len(frames)
    puzzle_part_length = int(math.sqrt(len(frames) / 3))
    
    size = (w, h) = (puzzle_part_length, ) * 2
    lake_frames.append(Image.fromstring("RGB", size, frames))

frames_length = int(math.sqrt(frames_length / 3))
size = (w, h) = (frames_length, ) * 2

lake_puzzle = Image.new("RGB", size, "white")
puzzle_size = frames_length / puzzle_part_length

for w in range(puzzle_size):
    for h in range(puzzle_size):
        part_location = h * puzzle_part_length, w * puzzle_part_length  
        lake_puzzle.paste(lake_frames[h + w * puzzle_size], part_location)

lake_puzzle.save("lake_puzzle.bmp")

print "Done, Level: 25"
