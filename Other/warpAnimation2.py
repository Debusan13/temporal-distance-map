import numpy as np
from skimage import io
import scipy.misc as smp
from scipy.interpolate import Rbf
from PIL import Image, ImageDraw, ImageFont
import imageio
import os
from scipy.spatial import cKDTree

mapResolution = 500

def dist(x1,y1,x2,y2):
    return ((x1-x2)**2+(y1-y2)**2)**0.5

def l2norm(x, y):
    if x == 0 and y == 0:
        return [0, 0]
    mag = (x**2+y**2)**0.5
    return [x/mag, y/mag]

def l1norm(x,y):
    if x == 0 and y == 0:
        return [0, 0]
    mag = abs(x)+abs(y)
    return [x/mag, y/mag]

dir_path = os.path.dirname(os.path.realpath(__file__))

image = io.imread(dir_path+'/geoImage.png')
rows, cols = image.shape[0], image.shape[1]

warpCoords = open(dir_path+'/warpFrames.txt').read().split('!')
importantPoints = open(dir_path+'/importantPoints.txt').read().split()
oneMinuteDistance = float(open(dir_path+'/minuteDistance.txt').read())

frameNumber = 0
images = []

if True:
    warpCoords = [warpCoords[0]]
#prev = 0
for warp in warpCoords:
    print(frameNumber)
    groups = warp.split()
    list_old_x, list_old_y, list_new_x, list_new_y = ([] for i in range(4))
    for group in groups:
        coords = group.split(',')
        list_old_x.append(float(coords[0]))
        list_old_y.append(float(coords[1]))
        list_new_x.append(float(coords[2]))
        list_new_y.append(float(coords[3]))

    array = np.array([list_new_x,list_new_y]).T
    tree = cKDTree(array)

    data = np.zeros( (mapResolution, mapResolution, 4), dtype=np.uint8 )

    for i in range(0, mapResolution):
        print(float(i)/mapResolution)
        for j in range(0, mapResolution):
            o = float(i)/mapResolution
            p = float(j)/mapResolution
            
            distances, ndx = tree.query([p,o], k=2)
            
            unnormDifVec = [list_new_x[ndx[0]]-list_new_x[ndx[1]], list_new_y[ndx[0]]-list_new_y[ndx[1]]]
            difVec = l2norm(unnormDifVec[0], unnormDifVec[1])
            centerDifVec = [p-0.5, o-0.5]
            normalized = l2norm(centerDifVec[0], centerDifVec[1])
            difDifVec = l2norm(p-list_new_x[ndx[1]], o-list_new_y[ndx[1]])
            projectedLength = (difDifVec[0]*unnormDifVec[0]+difDifVec[1]*unnormDifVec[1])/dist(unnormDifVec[0],unnormDifVec[1],0,0)
            if distances[0] == 0:
                print(projectedLength, difVec, difDifVec)
            mapDist = (1-projectedLength)*dist(list_old_x[ndx[1]],list_old_y[ndx[1]],0.5,0.5)+(projectedLength)*dist(list_old_x[ndx[0]],list_old_y[ndx[0]],0.5,0.5)
            unwarped_x = normalized[0]*mapDist+0.5
            unwarped_y = normalized[1]*mapDist+0.5

            if dist(unwarped_x, unwarped_y, 0.5, 0.5) < 0.01:
                color = [255,0,0,255]
            else:
                unwarped_x = int(unwarped_x * (rows-1))
                unwarped_y = int(unwarped_y * (cols-1))
                if unwarped_x < 0 or unwarped_x >= rows or unwarped_y < 0 or unwarped_y >= cols:
                    color = [0,0,0,0]
                else:
                    color = image[unwarped_x][unwarped_y]
            data[j, i] = color

    #labeling important points attempt
    img = smp.toimage( data )  # Create a PIL image
    # if frameNumber == 30:
    #     txt = Image.new('RGBA', (2055, 2048), (255, 255, 255, 0))
    #     fnt = ImageFont.truetype('C:/Users/lwsc2/PycharmProjects/untitled/venv/Lib/site-packages/matplotlib/mpl-data/fonts/ttf/DejaVuSans-Bold.ttf',7)
    #     draw = ImageDraw.Draw(img)
    #     for place in importantPoints:
    #         placeData = place.split(',')
    #         labelX = float(placeData[2]) * x
    #         labelY = (1.0 - float(placeData[1])) * y
    #         draw.text((labelX, labelY), str(placeData[0]), font=fnt, fill=(0, 0, 0))

    images.append(img)
    img.save(dir_path+'/Frames/map'+str(frameNumber)+'.png')
    frameNumber = frameNumber + 1

# images[1].save('C:/Users/lwsc2/Downloads/out3.gif', save_all = True, append_images = images, duration = 1, loop = 0)
# imageio.mimsave('C:/Users/lwsc2/Downloads/warpAnimationFromFile2.gif', images)
