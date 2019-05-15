import numpy as np
from skimage import io
import matplotlib.pyplot as plt
from skimage.transform import PiecewiseAffineTransform, warp
import scipy.misc as smp
from scipy.interpolate import Rbf
import random

image = io.imread('C:/Users/lwsc2/Downloads/geoImage.jpg')
rows, cols = image.shape[0], image.shape[1]
#2055x2048 pixel img

textfile = open('C:/Users/lwsc2/Downloads/warphighres.txt').read().split()

list_old_x, list_old_y, list_new_x, list_new_y = ([] for i in range(4))

for j in textfile:
    coords = j.split(',')
    list_old_x.append(float(coords[0]))
    list_old_y.append(float(coords[1]))
    list_new_x.append(float(coords[2]))
    list_new_y.append(float(coords[3]))

interpType= 'linear'
interpFunctionX = Rbf(list_new_x,list_new_y,list_old_x, function = interpType)
interpFunctionY = Rbf(list_new_x,list_new_y,list_old_y, function = interpType)

x = 2048
y = x

data = np.zeros( (x, y, 3), dtype=np.uint8 )

for i in range(0, y):
    print(i/y)
    for j in range(0, x):
        o = i/y
        p = j/x
        # closestPointDistance = 1000000000
        # for t in range(0,len(list_old_x)):
        #     distance=((list_new_x[t]-p)**2+(list_new_y[t]-o)**2)**0.5
        #     if distance < closestPointDistance:
        #         closestPointDistance = distance
        #         closestPoint = t
        unwarped_x = interpFunctionX(p,o)
        unwarped_y = interpFunctionY(p,o)
        unwarped_x = max(min(int(unwarped_x * (rows-1)),rows-1),0)
        unwarped_y = max(min(int(unwarped_y * (cols-1)),cols-1),0)
        color = image[unwarped_x][unwarped_y]
        data[j, i] = color

img = smp.toimage( data )  # Create a PIL image
img.save('C:/Users/lwsc2/Downloads/map.png')
img.show()                      # View in default viewer
