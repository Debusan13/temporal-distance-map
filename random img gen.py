import numpy as np
import scipy.misc as smp
import random

x = random.randint(1, 1025)
y = x

data = np.zeros( (x, y, 3), dtype=np.uint8 )

for i in range(0,y-1):
    for j in range(0,x-1):
        a = random.randint(0,255)
        b = random.randint(0,255)
        c = random.randint(0,255)
        data[i, j] = [a, b, c]

c1 = (255,0,0)
c2 = (0,255,0)
c3 = (0,0,255)

data[0] = c1
data[1] = c2
data[2] = c3

img = smp.toimage( data )       # Create a PIL image
img.show()                      # View in default viewer