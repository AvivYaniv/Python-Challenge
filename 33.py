import Image
import math

def GetHistogramPixelIndexes(histogram):
    histogram_pixel_indexes = []    
    for p in range(len(histogram)):
        if histogram[p] != 0:
            histogram_pixel_indexes.append(p)
    return histogram_pixel_indexes

def CovertListItemsToTuples(lst):
    tuples = []
    for i in range(0, len(lst)-1, 2):
        tuples.append((lst[i], lst[i+1]))
    return tuples

# Main
def main():
    beer = Image.open("beer2.png")
    w, h = beer.size
    total_pixels = (w * h)


    # OEIS A047239
    histogram_pixel_indexes = GetHistogramPixelIndexes(beer.histogram())

    pixel_indexes_tuples = CovertListItemsToTuples(histogram_pixel_indexes[::-1])

    data = list(beer.getdata())
    for t in range(len(pixel_indexes_tuples)-1):
        current_tuple = pixel_indexes_tuples[t]

        # If you are blinded by the light,
        # remove its power, with its might.
        arr = filter(lambda p: p not in current_tuple, data)

        s = math.sqrt(len(arr))

        # Then from the ashes, fair and square,        
        # another truth at you will glare.
        q = Image.new("L", (int(s), int(s)))
        q.putdata(arr)
        q.save("33_" + str(t) + ".jpg")

        data = arr

    print "Done level 33 :)"

if __name__ == "__main__":
    main()
