import numpy as np
import json
import math

from shapely.geometry import MultiPoint, Point, Polygon
import shapefile

data_dir = "data/050523"

#return a polygon for each state in a dictionary
def get_us_border_polygon():
    sf = shapefile.Reader("./data/cb_2018_us_state_500k.dbf")
    shapes = sf.shapes()
    #shapes[i].points
    fields = sf.fields
    records = sf.records()
    state_polygons = {}
    for i, record in enumerate(records):
        state = record[5]
        points = shapes[i].points
        poly = Polygon(points)
        state_polygons[state] = poly
    return state_polygons

#us border
state_polygons = get_us_border_polygon()   

#check if in one of the states then True, else False
def in_us(lon, lat):
    p = Point(lon, lat)
    for state, poly in state_polygons.items():
        if poly.contains(p):
            return state
    return None

# Define the latitude and longitude bounds of the contiguous United States
us_bounds = {
    'north': 49.3457868,
    'south': 24.7433195,
    'east': -66.9513812,
    'west': -124.7844079,
}

# Define the radius of the circles in meters
radius = 50000

# Define the distance between each grid point in degrees
degrees_per_meter = 1 / 111319.9
step = radius * degrees_per_meter * math.sqrt(3)

# Compute the number of rows and columns in the grid
num_rows = int(np.ceil((us_bounds['north'] - us_bounds['south']) / step))
num_cols = int(np.ceil((us_bounds['east'] - us_bounds['west']) / step))

# Compute the coordinates of the top-left corner of the grid
start_lat = us_bounds['north'] - num_rows * step
start_lng = us_bounds['west'] + num_cols * step

# Generate the grid of coordinates
coords = []
for i in range(num_rows):
    lat = start_lat + i * step
    for j in range(num_cols):
        lng = start_lng - j * step
        if us_bounds['south'] <= lat <= us_bounds['north'] and us_bounds['west'] <= lng <= us_bounds['east']:
        # if in_us(lng, lat):
            coords.append((lng, lat))



# Print the number of coordinates in the grid
print(len(coords))
json.dump(coords, open(f"{data_dir}/coordinates_contiguous_us.json", "w"))