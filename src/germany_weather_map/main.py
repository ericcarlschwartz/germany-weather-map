import requests
import numpy as np
import time

# 1. Define the bounds of Germany (approximate mainland)
LAT_MIN, LAT_MAX = 47.3, 55.0
LON_MIN, LON_MAX = 5.9, 15.0

# 2. Generate a grid of dots (e.g., 20x30 dots)
rows = 30
cols = 20
lats = np.linspace(LAT_MAX, LAT_MIN, rows)
lons = np.linspace(LON_MIN, LON_MAX, cols)

def fetch_weather_matrix():
    # Flatten grid for the API request
    grid_lats = []
    grid_lons = []
    for lat in lats:
        for lon in lons:
            grid_lats.append(round(lat, 2))
            grid_lons.append(round(lon, 2))

    # 3. Call Open-Meteo (DWD ICON-D2 Model)
    # The API supports batching multiple coordinates in one call
    url = "https://api.open-meteo.com/v1/dwd-icon"
    params = {
        "latitude": ",".join(map(str, grid_lats)),
        "longitude": ",".join(map(str, grid_lons)),
        "current": "temperature_2m,weather_code",
        "timezone": "Europe/Berlin"
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        
        # 4. Reshape data back into a matrix for your map
        matrix = []
        for i in range(rows):
            row_data = data[i*cols : (i+1)*cols]
            matrix.append(row_data)
        return matrix
    else:
        print(f"Error: {response.status_code}")
        return None

# Fetch and print a simple text-based "Temperature Map"
weather_data = fetch_weather_matrix()
if weather_data:
    print("--- Germany Temp Dot Matrix ---")
    for row in weather_data:
        # Simple visualization: Print a '.' if data exists
        line = ""
        for point in row:
            temp = point['current']['temperature_2m']
            # Color code logic could go here!
            line += f"{int(temp):3}° " 
        print(line)`
