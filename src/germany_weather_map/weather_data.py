import os
import time
import logging
import requests_cache
from urllib3.util import Retry
from requests.adapters import HTTPAdapter
from shapely.geometry import Point

from .map_utils import load_germany_boundary, lats, lons

logger = logging.getLogger(__name__)

# Global session singleton to leverage warm starts on Vercel
_session = None

def get_session(cache_backend=None):
    global _session
    if _session is not None:
        return _session

    # 1. Determine Backend & Connection String
    # Vercel KV provides KV_URL (starts with rediss://)
    redis_url = os.environ.get('KV_URL') or os.environ.get('REDIS_URL')
    
    backend = cache_backend or ('redis' if redis_url else 'sqlite')
    namespace = '.weather_cache'

    try:
        if backend == 'redis' and redis_url:
            logger.info("Initializing Redis cache backend")
            _session = requests_cache.CachedSession(
                namespace,
                backend='redis',
                connection=redis_url,
                expire_after=900,
                old_data_on_error=True
            )
        else:
            logger.info(f"Initializing {backend} cache backend")
            _session = requests_cache.CachedSession(
                namespace, 
                backend=backend,
                expire_after=900,
                old_data_on_error=True
            )
    except Exception as e:
        logger.warning(f"Failed to initialize '{backend}' cache backend, falling back to 'memory': {e}")
        _session = requests_cache.CachedSession(
            'weather_cache_mem',
            backend='memory',
            expire_after=900,
            old_data_on_error=True
        )
    
    # 2. Configure Retries
    retries = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    _session.mount('https://', HTTPAdapter(max_retries=retries))
    
    return _session

def fetch_weather_matrix(fast_mode=False, cache_backend=None):
    boundary = load_germany_boundary()
    
    grid_points = []
    points_to_query = []
    
    for lat in lats:
        row_points = []
        for lon in lons:
            point = Point(lon, lat)
            is_inside = boundary.contains(point) if boundary else True
            point_info = {"lat": round(lat, 2), "lon": round(lon, 2), "is_inside": is_inside, "data": None}
            row_points.append(point_info)
            if is_inside: points_to_query.append(point_info)
        grid_points.append(row_points)

    url = "https://api.open-meteo.com/v1/dwd-icon"
    batch_size = 500
    
    session = get_session(cache_backend=cache_backend)

    logger.info(f"Fetching weather data for {len(points_to_query)} points in batches of {batch_size}...")
    
    rate_limited = False
    for i in range(0, len(points_to_query), batch_size):
        batch = points_to_query[i : i + batch_size]
        batch_lats = [p["lat"] for p in batch]
        batch_lons = [p["lon"] for p in batch]

        params = {
            "latitude": ",".join(map(str, batch_lats)),
            "longitude": ",".join(map(str, batch_lons)),
            "current": "precipitation,temperature_2m,weather_code,cloud_cover",
            "timezone": "Europe/Berlin"
        }

        logger.info(f"  Batch {i//batch_size + 1}/{(len(points_to_query)-1)//batch_size + 1}...")
        try:
            if rate_limited:
                response = session.get(url, params=params, only_if_cached=True)
            else:
                response = session.get(url, params=params, timeout=15)

            if response.status_code == 200:
                is_from_cache = getattr(response, 'from_cache', False)
                if is_from_cache:
                    if getattr(response, 'is_expired', False):
                        logger.debug("loaded stale data from cache.")
                    else:
                        logger.debug("loaded from cache.")
                else:
                    logger.debug("fetched from API.")
                
                batch_data = response.json()
                if not isinstance(batch_data, list): batch_data = [batch_data]
                for point, data in zip(batch, batch_data): point["data"] = data
            elif response.status_code == 429:
                logger.error("Rate limited (429). Switching to cache-only mode.")
                rate_limited = True
                response = session.get(url, params=params, only_if_cached=True)
                if response.status_code == 200:
                    batch_data = response.json()
                    if not isinstance(batch_data, list): batch_data = [batch_data]
                    for point, data in zip(batch, batch_data): point["data"] = data
            else:
                logger.error(f"Error {response.status_code}.")

            if not getattr(response, 'from_cache', False) and not rate_limited and not fast_mode:
                time.sleep(2)
        except Exception as e:
            logger.error(f"Failed: {e}")

    is_complete = not any(p["data"] is None for p in points_to_query)
    if not is_complete:
        logger.warning("Some points could not be fetched.")

    return grid_points, is_complete
