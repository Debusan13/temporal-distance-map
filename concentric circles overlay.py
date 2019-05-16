import numpy as np
from skimage import io
import scipy.misc as smp
from scipy.interpolate import Rbf
from PIL import ImageDraw, Image, ImageFont
import cv2

image = io.imread('C:/Users/lwsc2/Downloads/geoImage.jpg')
rows, cols = image.shape[0], image.shape[1]
#2055x2048 pixel img

textfile = open('C:/Users/lwsc2/Downloads/lastFrame.txt').read().split()

list_old_x, list_old_y, list_new_x, list_new_y = ([] for i in range(4))

for j in textfile:
    coords = j.split(',')
    list_old_x.append(float(coords[0]))
    list_old_y.append(float(coords[1]))
    list_new_x.append(float(coords[2]))
    list_new_y.append(float(coords[3]))

for i in range(0,len(list_old_x)):
    if list_old_x[i]==0.5 and list_old_y[i]==0.5:
        centerPointIndex = i
centerPointPosition = [list_new_x[centerPointIndex],list_new_y[centerPointIndex]]

interpType= 'linear'
interpFunctionX = Rbf(list_new_x,list_new_y,list_old_x, function = interpType)
interpFunctionY = Rbf(list_new_x,list_new_y,list_old_y, function = interpType)

#2048
x = 100
y = x

data = np.zeros( (x, y, 3), dtype=np.uint8 )

for i in range(0, y):
    print(i / y)
    for j in range(0, x):
        o = i / y
        p = j / x
        unwarped_x = interpFunctionX(p, o)
        unwarped_y = interpFunctionY(p, o)
        if ((unwarped_x - centerPointPosition[0]) ** 2 + (unwarped_y - centerPointPosition[1]) ** 2) ** 0.5 < 0.01:
            color = [255, 0, 0]
        else:
            unwarped_x = int(unwarped_x * (rows - 1))
            unwarped_y = int(unwarped_y * (cols - 1))
            if unwarped_x < 0 or unwarped_x >= rows or unwarped_y < 0 or unwarped_y >= cols:
                color = [0, 0, 0]
            else:
                color = image[unwarped_x][unwarped_y]
        data[j, i] = (color[2], color[1], color[0])  #using cv2 for imaging, color vals are BGR

r = int(x/100) # radius = 1/100 of image size
for k in range(r, x, r):
    cv2.circle(data, (int(x/2), int(x/2)), k, (0, 0, 255), 1)

cv2.imwrite('C:/Users/lwsc2/Downloads/cvmap.png', data)
cv2.imshow('Output', data)
cv2.waitKey(0)
