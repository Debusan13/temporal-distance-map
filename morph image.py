import numpy as np
from skimage import io
import matplotlib.pyplot as plt
from skimage.transform import PiecewiseAffineTransform, warp
import scipy.misc as smp
import random

image = io.imread('C:/Users/lwsc2/Downloads/geoImage.jpg')
rows, cols = image.shape[0], image.shape[1]

print(rows, cols)

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

data = np.zeros( (x, y, 3), dtype=np.uint8 )

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
        unwarped_x = list_old_x[closestPoint]
        unwarped_y = list_old_y[closestPoint]
        unwarped_x = min(int(unwarped_x * rows), rows)
        unwarped_y = min(int(unwarped_y * cols), cols)
        color = image[unwarped_x-1][unwarped_y-1]
        data[i, j] = color

img = smp.toimage( data )       # Create a PIL image
img.show()                      # View in default viewer
