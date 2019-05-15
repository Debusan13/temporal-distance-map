import numpy as np
import scipy.misc as smp
import random

textfile = open('C:/Users/lwsc2/Downloads/warp.txt').read().split()

list_old_x, list_old_y, list_new_x, list_new_y = ([] for i in range(4))

for j in textfile:
    coords = j.split(',')
    list_old_x.append(float(coords[0]))
    list_old_y.append(float(coords[1]))
    list_new_x.append(float(coords[2]))
    list_new_y.append(float(coords[3]))

x = 100
y = x

#data = np.zeros( (x, y, 3), dtype=np.uint8 )

for i in range(0, y-1):
    for j in range(0, x-1):
        o = i/y
        p = j/x
        closestPoint = 0
        closestPointDistance = ((list_new_x[0]-p)**2+(list_new_y[0]-o)**2)**0.5
        for t in range(0,49):
            distance=((list_new_x[t]-p)**2+(list_new_y[t]-o)**2)**0.5
            if distance < closestPointDistance:
                closestPointDistance = distance
                closestPoint = t
        print(closestPoint)

        a = random.randint(0,255)  #we don't want random in the actual thing
        b = random.randint(0,255)
        c = random.randint(0,255)
        #data[i, j] = [a, b, c]

#img = smp.toimage( data )       # Create a PIL image
#img.show()                      # View in default viewer
