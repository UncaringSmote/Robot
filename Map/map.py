import geopy
from geopy import distance
from path import Path

# given: lat1, lon1, b = bearing in degrees, d = distance in kilometers
initial_lat_lon=(30.5183237847436, -84.2486411333084)
initial_brn = 90
Path(initial_lat_lon,initial_brn)
