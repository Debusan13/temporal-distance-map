import numpy as np
import random
from skimage import io
import scipy.misc as smp
from scipy.interpolate import Rbf
from PIL import Image, ImageDraw, ImageFont
import imageio
import os
from datetime import datetime
import threading

mapResolution = 500
ringMinutes = 300
frames = 3
matchScale = False
framesToRender = list(range(0, frames+1))
#framesToRender = [0, frames]

def dist(x1,y1,x2,y2):
    return ((x1-x2)**2+(y1-y2)**2)**0.5

def l2norm(x, y):
    if x == 0 and y == 0:
        return [0, 0]
    mag = (x**2+y**2)**0.5
    return [x/mag, y/mag]

unit = "minute"
convertedRings = ringMinutes
if convertedRings%60 == 0:
    convertedRings = convertedRings/60
    unit = "hour"
if convertedRings != 1:
    unit = unit+"s"
legendText = "Each contour represents "+str(convertedRings)+" more "+unit+" from the center"

dir_path = os.path.dirname(os.path.realpath(__file__))

image = io.imread(dir_path+'/geoImage.png')
rows, cols = image.shape[0], image.shape[1]

warp = open(dir_path+'/warpMesh.txt').read()
importantPoints = open(dir_path+'/importantPoints.txt').read().split('\n')
oneMinuteDistance = float(open(dir_path+'/minuteDistance.txt').read())
if matchScale:
    matchMeshScale = float(open(dir_path+'/matchMeshScale.txt').read())
else:
    matchMeshScale = 1

#images = []
groups = warp.split()
list_old_x, list_old_y, list_new_x, list_new_y, list_old_dist, list_new_dist = ([] for i in range(6))
for group in groups:
    coords = group.split(',')
    list_old_x.append(float(coords[0]))
    list_old_y.append(float(coords[1]))
    list_new_x.append(float(coords[2]))
    list_new_y.append(float(coords[3])+random.random()/1000000)
    list_old_dist.append(dist(list_old_x[-1],list_old_y[-1],0.5,0.5))
    list_new_dist.append(dist(list_new_x[-1],list_new_y[-1],0.5,0.5))

interpType= 'linear'
interpFunctionOldDist = Rbf(list_new_x,list_new_y,list_old_dist, function = interpType)

cache = dict()

for i in range(0, mapResolution):
    for j in range(0, mapResolution):
        o = float(i)/mapResolution
        p = float(j)/mapResolution
        cache[(1-p, o)] = interpFunctionOldDist(1-p, o)

for place in importantPoints:
    placeData = place.split(',')
    if len(placeData) >= 3:
        p = float(placeData[1])
        o = float(placeData[2])
        cache[(p, o)] = interpFunctionOldDist(p, o)

interpFunctionNewDist = Rbf(list_old_x,list_old_y,list_new_dist, function = interpType)

ringDist = oneMinuteDistance*ringMinutes

class RenderFrame(threading.Thread):
    def __init__ (self, frameNum, oldDistCache):
        threading.Thread.__init__(self)
        self.frameNumber = frameNum
        self.oldDistCache = oldDistCache
    
    def run(self):
        global renderProgress
        progress = float(self.frameNumber)/frames
        data = np.zeros( (mapResolution, mapResolution, 4), dtype=np.uint8 )
        
        for i in range(0, mapResolution):
            timeProgress = renderProgress/(mapResolution*len(framesToRender))
            if timeProgress > 0:
                curTime = datetime.now()
                print("Approximately "+"{0:.2f}".format((curTime-startTime).total_seconds()*(1-timeProgress)/timeProgress)+" seconds remaining")
            for j in range(0, mapResolution):
                o = float(i)/mapResolution
                p = float(j)/mapResolution
                
                curDist = dist(p, o, 0.5, 0.5)
                
                if curDist < 0.002:
                    color = [255,0,0,255]
                else:
                    oldDist = self.oldDistCache[(1-p, o)]
                    normalized = l2norm(p-0.5, o-0.5)
                    
                    mapDist = oldDist*progress+(1-progress)*curDist/matchMeshScale
                    unwarped_x = normalized[0]*mapDist+0.5
                    unwarped_y = normalized[1]*mapDist+0.5
                    
                    if unwarped_x < 0 or unwarped_x > 1 or unwarped_y < 0 or unwarped_y > 1:
                        color = [255,255,255,0]
                    else:
                        newDist = interpFunctionNewDist(1-unwarped_x, unwarped_y)
                        
                        unwarped_x = int(unwarped_x * (rows-1))
                        unwarped_y = int(unwarped_y * (cols-1))
                        
                        color = image[unwarped_x][unwarped_y]
                        
                        circleDist = (newDist*(1-progress)+curDist*progress)
                        if circleDist % ringDist < 0.002:
                            color = [(color[0]+128)/2, (color[1]+128)/2, (color[2]+128)/2, color[3]]
            
                data[j, i] = color
            renderProgress = renderProgress + 1

        img = Image.fromarray(data)
        
        txt = Image.new('RGBA', (2055, 2048), (255, 255, 255, 0))
        fnt = ImageFont.truetype(dir_path+'/Roboto/Roboto-Regular.ttf', max(int(0.02*mapResolution), 10))
        draw = ImageDraw.Draw(img)
        for place in importantPoints:
            placeData = place.split(',')
            if len(placeData) >= 3:
                p = float(placeData[1])
                o = float(placeData[2])
                oldDist = self.oldDistCache[(p, o)]
                normalized = l2norm(p-0.5, o-0.5)
                curDist = dist(p, o, 0.5, 0.5)
                mapDist = oldDist*(1-progress)+progress*curDist
                mapDist = mapDist*(matchMeshScale*(1-progress)+progress)
                unwarped_x = normalized[0]*mapDist+0.5
                unwarped_y = normalized[1]*mapDist+0.5
                labelX = unwarped_y * mapResolution
                labelY = (1-unwarped_x) * mapResolution
                draw.text((labelX, labelY), str(placeData[0]), font=fnt, fill=(0, 0, 0))
                draw.text((0, 0), legendText, font=fnt, fill=(0, 0, 0))

        img.save(dir_path+'/Frames/map'+str(self.frameNumber)+'.png')

renderProgress = 0
startTime = datetime.now()
threads = []
for frameNum in framesToRender:
    thread = RenderFrame(frameNum, cache)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

