import argparse
import requests
import numpy as np
import time
import json
from shapely.geometry import shape, Point
import requests_cache
from retry_requests import retry

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
    # Batch size of 100 is a good balance for URI length and rate limits
    batch_size = 100
    url = "https://api.open-meteo.com/v1/dwd-icon"

    # Setup caching and retries
    # Cache expires after 15 minutes
    session = requests_cache.CachedSession('.weather_cache', expire_after=900)
    
    # Configure retries with exponential backoff
    from urllib3.util import Retry
    from requests.adapters import HTTPAdapter
    
    retries = Retry(
        total=5,
        backoff_factor=1,  # 1s, 2s, 4s, 8s, 16s
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    session.mount('https://', HTTPAdapter(max_retries=retries))

    print(f"Fetching weather data for {len(points_to_query)} points in batches of {batch_size}...")
    
    for i in range(0, len(points_to_query), batch_size):
        batch = points_to_query[i : i + batch_size]
        batch_lats = [p["lat"] for p in batch]
        batch_lons = [p["lon"] for p in batch]

        params = {
            "latitude": ",".join(map(str, batch_lats)),
            "longitude": ",".join(map(str, batch_lons)),
            "current": "precipitation,temperature_2m,weather_code",
            "timezone": "Europe/Berlin"
        }

        print(f"  Batch {i//batch_size + 1}/{(len(points_to_query)-1)//batch_size + 1}...", end=" ", flush=True)
        try:
            response = session.get(url, params=params, timeout=15)
            if response.status_code == 200:
                if getattr(response, 'from_cache', False):
                    print("loaded from cache.")
                else:
                    print("fetched from API.")
                
                batch_data = response.json()
                if not isinstance(batch_data, list):
                    batch_data = [batch_data]
                for point, data in zip(batch, batch_data):
                    point["data"] = data
            elif response.status_code == 429:
                print("Rate limited (429). Daily limit reached.")
                break # Stop if we are definitely rate limited for the day
            else:
                print(f"Error {response.status_code}.")

            # If not from cache, wait to stay under the 600/min limit
            if not getattr(response, 'from_cache', False):
                time.sleep(2)
        except Exception as e:
            print(f"Failed: {e}")



    if any(p["data"] is None for p in points_to_query):
        print("\nNote: Some points could not be fetched (likely due to API rate limits).")
        print("The map below may show '?' for these locations.\n")

    return grid_points

def get_precip_color(precip):
    if precip <= 0:
        return " .  "
    
    # ANSI background colors for radar-like visualization
    if precip < 0.5:
        color = "\033[46m"  # Cyan: Light rain
    elif precip < 2.0:
        color = "\033[44m"  # Blue: Moderate rain
    elif precip < 5.0:
        color = "\033[42m"  # Green: Heavy rain
    elif precip < 10.0:
        color = "\033[43m"  # Yellow: Very heavy rain
    elif precip < 20.0:
        color = "\033[41m"  # Red: Intense rain
    else:
        color = "\033[45m"  # Magenta: Extreme rain
        
    return f"{color}   \033[0m "

def get_temp_color(temp):
    # 12Tempera Color Scheme (Smoothed 12-bin transition)
    # Mapping based on typical meteorological transitions: Purple -> Blue -> Cyan -> Green -> Yellow -> Orange -> Red
    if temp < -10:
        color = "\033[48;5;57m"   # Deep Purple
    elif temp < -5:
        color = "\033[48;5;63m"   # Purple-Blue
    elif temp < 0:
        color = "\033[48;5;33m"   # Blue
    elif temp < 5:
        color = "\033[48;5;39m"   # Light Blue
    elif temp < 10:
        color = "\033[48;5;45m"   # Cyan
    elif temp < 15:
        color = "\033[48;5;40m"   # Green
    elif temp < 20:
        color = "\033[48;5;118m"  # Light Green
    elif temp < 25:
        color = "\033[48;5;226m"  # Yellow
    elif temp < 30:
        color = "\033[48;5;220m"  # Gold / Dark Yellow
    elif temp < 35:
        color = "\033[48;5;214m"  # Orange
    elif temp < 40:
        color = "\033[48;5;202m"  # Orange-Red
    else:
        color = "\033[48;5;196m"  # Bright Red

    return f"{color}   \033[0m "

def main():
    parser = argparse.ArgumentParser(description="Germany Weather Map")
    parser.add_argument(
        "map_type", 
        choices=["temp", "precip"], 
        nargs="?", 
        default="temp",
        help="Type of map to display: 'temp' for temperature or 'precip' for precipitation (default: temp)"
    )
    args = parser.parse_args()

    weather_data = fetch_weather_matrix()
    if not weather_data:
        return

    if args.map_type == "precip":
        print("\n--- Germany Precipitation Doppler Radar ---")
        print(" Legend: \033[46m   \033[0m <0.5mm, \033[44m   \033[0m <2mm, \033[42m   \033[0m <5mm, \033[43m   \033[0m <10mm, \033[41m   \033[0m <20mm, \033[45m   \033[0m 20mm+")
        print(" (x = outside boundary, . = 0mm) \n")
        
        for row in weather_data:
            line = ""
            for point in row:
                if not point["is_inside"]:
                    line += " x  "
                elif point["data"]:
                    precip = point["data"]['current']['precipitation']
                    line += get_precip_color(precip)
                else:
                    line += " ?  " 
            print(line)
    else:
        print("\n--- Germany Temperature Map (12Tempera) ---")
        print(" Legend: \033[48;5;57m   \033[0m <-10°C, \033[48;5;63m   \033[0m <-5°C, \033[48;5;33m   \033[0m <0°C, \033[48;5;39m   \033[0m <5°C, \033[48;5;45m   \033[0m <10°C, \033[48;5;40m   \033[0m <15°C,")
        print("         \033[48;5;118m   \033[0m <20°C, \033[48;5;226m   \033[0m <25°C, \033[48;5;220m   \033[0m <30°C, \033[48;5;214m   \033[0m <35°C, \033[48;5;202m   \033[0m <40°C, \033[48;5;196m   \033[0m 40°C+")
        print(" (x = outside boundary) \n")
        
        for row in weather_data:
            line = ""
            for point in row:
                if not point["is_inside"]:
                    line += " x  "
                elif point["data"]:
                    temp = point["data"]['current']['temperature_2m']
                    line += get_temp_color(temp)
                else:
                    line += " ?  " 
            print(line)

if __name__ == "__main__":
    main()
