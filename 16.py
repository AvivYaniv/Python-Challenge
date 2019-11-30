import sys
from PIL import Image
import itertools

im = Image.open('mozart.gif').convert('RGB')
width, height = im.size
pixels = list(im.getdata())

# Image to Matrix
w=0
d=w / width
im_mat=[list([0])] * width
while d <= height:
    nw=w+width
    im_mat[w / width]=pixels[w:nw]
    d=w / width
    w=nw

s=[(255, 0, 255), (255, 0, 255), (255, 0, 255), (255, 0, 255), (255, 0, 255)]

al_mat=[]

for row in range(height):
    index = 0
    r=list(im_mat[row])

    for i in range(len(r)):
        if r[i:i+len(s)] == s:
            index = i
            break
        
    if index == 0:
        al_mat.extend(r)
    else:
        a=list(r[0:index])       
        b=list(r[index:len(r)])
        b.extend(a)  
        al_mat.extend(b)        


al=Image.new('RGB', (width, height))
al.putdata(al_mat)
al.save('aligned.gif')
