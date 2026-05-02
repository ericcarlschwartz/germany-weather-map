import requests
import numpy as np
import time
import json
from shapely.geometry import shape, Point

# 1. Define the bounds of Germany (approximate mainland)
LAT_MIN, LAT_MAX = 47.3, 55.0
LON_MIN, LON_MAX = 5.9, 15.0

# 2. Generate a grid of dots (e.g., 30x45 dots for better performance)
rows = 45
cols = 30
lats = np.linspace(LAT_MAX, LAT_MIN, rows)
lons = np.linspace(LON_MIN, LON_MAX, cols)

def load_germany_boundary():
    try:
        with open("germany.json", "r") as f:
            data = json.load(f)
            # Assuming the first feature is the country boundary
            return shape(data['features'][0]['geometry'])
    except Exception as e:
        print(f"Error loading GeoJSON: {e}")
        return None

def fetch_weather_matrix():
    boundary = load_germany_boundary()
    
    # Identify which points are inside Germany
    grid_points = []
    points_to_query = []
    
    for lat in lats:
        row_points = []
        for lon in lons:
            point = Point(lon, lat)
            is_inside = boundary.contains(point) if boundary else True
            
            point_info = {
                "lat": round(lat, 2),
                "lon": round(lon, 2),
                "is_inside": is_inside,
                "data": None
            }
            row_points.append(point_info)
            if is_inside:
                points_to_query.append(point_info)
        grid_points.append(row_points)

    # 3. Call Open-Meteo (DWD ICON-D2 Model)
    # Batch size of 100 is efficient and stays within Open-Meteo's URI and rate limits
    batch_size = 100
    url = "https://api.open-meteo.com/v1/dwd-icon"

    for i in range(0, len(points_to_query), batch_size):
        batch = points_to_query[i : i + batch_size]
        batch_lats = [p["lat"] for p in batch]
        batch_lons = [p["lon"] for p in batch]

        params = {
            "latitude": ",".join(map(str, batch_lats)),
            "longitude": ",".join(map(str, batch_lons)),
            "current": "precipitation,weather_code",
            "timezone": "Europe/Berlin"
        }

        # Retry logic for rate limits with true exponential backoff
        max_retries = 10
        for retry in range(max_retries):
            response = requests.get(url, params=params)
            if response.status_code == 200:
                batch_data = response.json()
                if not isinstance(batch_data, list):
                    batch_data = [batch_data]
                for point, data in zip(batch, batch_data):
                    point["data"] = data
                break
            elif response.status_code == 429:
                wait_time = min(2**retry, 60)
                print(f"Rate limited (429). Waiting {wait_time}s before retry {retry+1}/{max_retries}...")
                time.sleep(wait_time)
            else:
                print(f"Error: {response.status_code} at batch {i//batch_size}")
                break

        # Base sleep of 0.1s is sufficient for the 600 calls/min limit
        time.sleep(0.1)


    return grid_points

# Fetch and print a simple text-based "Precipitation Map"
weather_data = fetch_weather_matrix()
if weather_data:
    print("--- Germany Precipitation Dot Matrix (mm) ---")
    print(" (x = outside boundary, . = 0mm) ")
    for row in weather_data:
        line = ""
        for point in row:
            if not point["is_inside"]:
                line += " x  "
            elif point["data"]:
                precip = point["data"]['current']['precipitation']
                if precip > 0:
                    line += f"{precip:3.1f} " 
                else:
                    line += " .  "
            else:
                line += " ?  " # Data missing or error
        print(line)
