import json
import numpy as np
from pathlib import Path
from shapely.geometry import shape

# Define base path for data files
DATA_DIR = Path(__file__).parent.parent.parent
GERMANY_JSON = DATA_DIR / "germany.json"

# Define the bounds of Germany (approximate mainland)
LAT_MIN, LAT_MAX = 47.3, 55.0
LON_MIN, LON_MAX = 5.9, 15.0

# Generate a grid of dots
ROWS = 64
COLS = 32

def generate_grid():
    # Padding of 2 rows/cols on each side
    # The original LAT/LON bounds should correspond to index 2 and index size-3
    d_lat = (LAT_MAX - LAT_MIN) / (ROWS - 5)
    d_lon = (LON_MAX - LON_MIN) / (COLS - 5)

    lat_max_pad = LAT_MAX + 2 * d_lat
    lat_min_pad = LAT_MIN - 2 * d_lat
    lon_min_pad = LON_MIN - 2 * d_lon
    lon_max_pad = LON_MAX + 2 * d_lon

    lats = np.linspace(lat_max_pad, lat_min_pad, ROWS)
    lons = np.linspace(lon_min_pad, lon_max_pad, COLS)
    return lats, lons

lats, lons = generate_grid()

def load_germany_boundary():
    try:
        with open(GERMANY_JSON, "r") as f:
            data = json.load(f)
            # Assuming the first feature is the country boundary
            return shape(data['features'][0]['geometry'])
    except Exception as e:
        import logging
        logging.error(f"Error loading GeoJSON: {e}")
        return None
