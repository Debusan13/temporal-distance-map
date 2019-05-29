# Temporal Distance Map
Blake Albert, Christian Panici, Nigel Castelino

## Abstract

Some map projections preserve distance to create a physical representation of a given area; however, people are generally more concerned with the time it takes to reach a destination rather than their physical distance to it. Currently, isochrone maps can display travel times, but they are only an overlay over the original map rather than a transformation. We use Python along with travel time data from Wolfram Language to transform a map that preserves distance into one that proportionately displays locations based on the time it takes to travel there from a given point. Our transformed map allows for different analyses on the efficiency of travel in different areas. To the best of our knowledge, this is a unique method of generating a map that gives a possibly more compelling visualization of travel time when compared to isochrone maps.

## Documentation

Open Temporal Distance Map.nb and run GenerateWarpMesh. Export files using code under the section “Export files”. Run warpAnimation.py under “Warp” in the notebook, or run it in the command line. If making an animation, run makeAnimation.py.

```
GenerateWarpMesh[center, radius, resolution, importantPoints]:
  center - a GeoPositon marking the center of the map to compute travel time from
  radius - a length Quantity for how far from the center the map should encapsulate
  resolution - a length Quantity for how far apart the grid’s mesh points should be
  importantPoints (optional) - a list of form {{name, coordinates}} where the name should be placed at coordinates on the map. Most populous cities in the area will be chosen if this is left out.

warpAnimation.py resolution ringMinutes frameCount matchScale frames
  resolution - the resolution of the final image will be resolution*resolution
  ringMinutes - how many minutes the contours should be apart
  frameCount - the length of the animation in frames
  matchScale - determines if the map should be shrinked at the beginning to roughly match its size at the end of the animation
  frames - which frames to generate {“first”, “last”, “all”}
  ```
