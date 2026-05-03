import json
import numpy as np
from shapely.geometry import shape, Point

# 1. Define the bounds of Germany (approximate mainland)
LAT_MIN, LAT_MAX = 47.3, 55.0
LON_MIN, LON_MAX = 5.9, 15.0

# 2. Generate a grid of dots
rows = 64
cols = 32

# Padding of 2 rows/cols on each side
# The original LAT/LON bounds should correspond to index 2 and index size-3
d_lat = (LAT_MAX - LAT_MIN) / (rows - 5)
d_lon = (LON_MAX - LON_MIN) / (cols - 5)

LAT_MAX_PAD = LAT_MAX + 2 * d_lat
LAT_MIN_PAD = LAT_MIN - 2 * d_lat
LON_MIN_PAD = LON_MIN - 2 * d_lon
LON_MAX_PAD = LON_MAX + 2 * d_lon

lats = np.linspace(LAT_MAX_PAD, LAT_MIN_PAD, rows)
lons = np.linspace(LON_MIN_PAD, LON_MAX_PAD, cols)

def load_germany_boundary():
    try:
        with open("germany.json", "r") as f:
            data = json.load(f)
            # Assuming the first feature is the country boundary
            return shape(data['features'][0]['geometry'])
    except Exception as e:
        print(f"Error loading GeoJSON: {e}")
        return None
