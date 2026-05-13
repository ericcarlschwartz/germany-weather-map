import time
import logging
import requests_cache
from urllib3.util import Retry
from requests.adapters import HTTPAdapter
from shapely.geometry import Point

from .map_utils import load_germany_boundary, lats, lons

logger = logging.getLogger(__name__)

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

    # Call Open-Meteo (DWD ICON-D2 Model)
    batch_size = 100
    url = "https://api.open-meteo.com/v1/dwd-icon"

    # Setup caching and retries
    session = requests_cache.CachedSession('.weather_cache', expire_after=900)
    
    retries = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    session.mount('https://', HTTPAdapter(max_retries=retries))

    logger.info(f"Fetching weather data for {len(points_to_query)} points in batches of {batch_size}...")
    
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

        logger.info(f"  Batch {i//batch_size + 1}/{(len(points_to_query)-1)//batch_size + 1}...")
        try:
            response = session.get(url, params=params, timeout=15)
            if response.status_code == 200:
                if getattr(response, 'from_cache', False):
                    logger.debug("loaded from cache.")
                else:
                    logger.debug("fetched from API.")
                
                batch_data = response.json()
                if not isinstance(batch_data, list):
                    batch_data = [batch_data]
                for point, data in zip(batch, batch_data):
                    point["data"] = data
            elif response.status_code == 429:
                logger.error("Rate limited (429). Daily limit reached.")
                break 
            else:
                logger.error(f"Error {response.status_code}.")

            if not getattr(response, 'from_cache', False):
                time.sleep(2)
        except Exception as e:
            logger.error(f"Failed: {e}")

    if any(p["data"] is None for p in points_to_query):
        logger.warning("Some points could not be fetched.")

    return grid_points
