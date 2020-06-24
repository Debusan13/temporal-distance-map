# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 10:58:06 2020

@author: Eli Nacar
"""

import numpy as np
import requests
import math 
import json

#Gets the image and its bounds
orig_lat = 25.7617
orig_long = -80.1918

KEY = "AqRZj36O-xKG58fcI123-xJGxM76_CuITqN7-hRXqAI2Kbeh2yD_vv1d7U9hMZOD"
ZOOM = "11"
URL = "https://dev.virtualearth.net/REST/V1/Imagery/Map/Road/" + str(orig_lat) + "%2C" + str(orig_long) + "/" + ZOOM + "?mapSize=2048,2048&dpi=Large&format=png&key=" + KEY

response = requests.get(URL)

#gets image
#writes image to file name
with open('geoImage.png', 'wb') as file:
       file.write(response.content)

#gets image metadata
URL_M = "https://dev.virtualearth.net/REST/V1/Imagery/Map/Road/" + str(orig_lat) + "%2C" + str(orig_long) + "/" + ZOOM + "?mapSize=2048,2048&mapMetadata=1&o=json&key=" + KEY
response = requests.get(URL_M)

jsonResponse = response.json()
#array w/ long + lat bounds
bounds = jsonResponse['resourceSets'][0]['resources'][0]['bbox']

##############################################################################################
#Mesh based on ratio of max longitude(x-axis) and latitude(y-axis)

southLat = bounds[0]
westLong = bounds[1]
northLat = bounds[2]
eastLong = bounds[3]

#Total Longitude and Latitude depicted on map
latDiff = northLat - southLat
longDiff = eastLong - westLong

#Interval of movement along the euclidean plane
latMove = latDiff * .03125
longMove = longDiff * .03125

#Creation of the mesh of points (.03125 interval excluding all 0s and 1s)
mesh = np.zeros((961, 7), dtype=float) #style [old latitude, old longitude, travel_time, old_x, old_y, new_x, new_y]

x_counter = 1
y_counter = 1

#Creates a mesh of points by going through x-axis and creating points along the y-axis
for i in mesh:
    i[0] = southLat + latMove * y_counter #moves north incrementally
    i[1] = westLong + longMove * x_counter #moves east incrementally
    i[3] = 0 + .03125 * x_counter #moves along x-axis
    i[4] = 0 + .03125 * y_counter #moves along y-axis
    
    y_counter += 1
    if (y_counter == 32):
        x_counter += 1
        y_counter = 1

###################################################################################################
#Calculate Travel Time for every point (minutes)
    
URL = "https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?key=" + KEY

#Coordinates for point with the largest travel time
maxDistance = np.zeros([7], dtype=float)

#--priming payload w/ each longitude & lattitude--
latitude = []
longitude = []
for item in mesh:
    latitude.append(item[0])
for item in mesh:
    longitude.append(item[1])

travelTimes = []
coords = []
for x in range(0, 961):
    coord = {'latitude': latitude[x], 'longitude': longitude[x]}
    coords.append(coord)

payload = {'origins': [{'latitude':orig_lat, 'longitude':orig_long}],'destinations':coords,'travelMode':'driving','timeUnit':'minute'}

#--getting travel times from the origin to each destination
    
r = requests.post(URL, json=payload)
json_r = r.json()
#parses "results" out of json object
results = json_r['resourceSets'][0]['resources'][0]['results']
#gets "travelDuration" key out of each obj in results array
for result in results :
    travelTimes.append(result['travelDuration'])
    
for i in range(0, len(mesh)):
    mesh[i][2] = travelTimes[i]
    if (travelTimes[i] > maxDistance[2]):
        maxDistance = mesh[i]

    
###################################################################################################
#Calculation for imPoints
        
#Could be an additional implementation        

###################################################################################################
#Calculate Minute Distance

largestDistance = math.sqrt((maxDistance[3] - 0.5)**2 + (maxDistance[4] - 0.5)**2)

OneMinuteDistance = largestDistance/maxDistance[2]
        
###################################################################################################
#Find angle to each point and move based on minute distance/travel time

warpMesh = open("warpMesh.txt", "w") 
minuteDistance = open("minuteDistance.txt", "w")

for i in mesh:
    distance = i[2] * OneMinuteDistance
    angle = math.atan2(i[4] - .5, i[3] - .5)
    i[5] = .5 + (distance * math.cos(angle))
    i[6] = .5 + (distance * math.sin(angle))
    
    warpMesh.write("%f,%f,%f,%f\n" % (i[3], i[4], i[5], i[6]))
    
minuteDistance.write("%f\n" % OneMinuteDistance)
    
warpMesh.close()
minuteDistance.close()