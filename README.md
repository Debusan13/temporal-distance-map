# temporal-distance-map

## Web Application

Link to the repository for the [web application](https://github.com/Debusan13/temporal-distance-map-web)

## Installation Guide

#### 1. Setting up the environment
   1. Install [Mini Conda](https://docs.conda.io/en/latest/miniconda.html)
   2. Create a new environment and install the following packages and their dependencies
      * Scipy
      * NumPy
      * Pillow
      * Requests
      * JSON
      * imageio
      * skimage
      
      
   3. Activate the environment

#### 2. Running the code
   1. Go to <https://www.bingmapsportal.com/> and create an API key
   2. In [MapLogic.py](https://github.com/Debusan13/temporal-distance-map/blob/master/MapLogic.py), change the variable KEY to your API key in type string
   3. Change the 'orig_lat' and 'orig_long' variables to the latitude and longitude of the location you want to transform
   4. Run 'MapLogic.py'
   5. Run 'warpAnimation.py'
   6. Run 'makeAnimation.py'

## Poster
![](https://github.com/Debusan13/temporal-distance-map/blob/master/temporal_distnace_map_poster-1.png)
