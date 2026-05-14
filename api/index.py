import os
import sys
import logging

# Set up logging to stdout so it appears in Vercel logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the project root and src directory to sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
src_path = os.path.join(root_path, "src")
sys.path.insert(0, src_path)
sys.path.insert(0, root_path)

try:
    from germany_weather_map.weather_data import fetch_weather_matrix
    from germany_weather_map.display import create_framebuffer, render_map_to_html
    logger.info("Successfully imported germany_weather_map modules")
except ImportError as e:
    logger.error(f"Failed to import modules: {e}")
    raise

from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse

app = FastAPI()

# Vercel Cache headers: 15 minutes fresh, 5 minutes stale-while-revalidate
CACHE_HEADER = {"Cache-Control": "s-maxage=900, stale-while-revalidate=300"}

@app.get("/", response_class=HTMLResponse)
@app.get("/api/preview", response_class=HTMLResponse)
def preview_map(map_type: str = "temp"):
    data = fetch_weather_matrix(fast_mode=True, cache_backend='memory')
    fb = create_framebuffer(data, map_type=map_type)
    html_content = render_map_to_html(data, fb, map_type=map_type)
    return HTMLResponse(content=html_content, headers=CACHE_HEADER)

@app.get("/api/weather")
def get_weather_binary(map_type: str = "temp"):
    # fast_mode=True to avoid Vercel timeout (10s limit)
    # cache_backend='memory' for read-only filesystem
    data = fetch_weather_matrix(fast_mode=True, cache_backend='memory')
    fb = create_framebuffer(data, map_type=map_type)
    return Response(content=fb.tobytes(), media_type="application/octet-stream", headers=CACHE_HEADER)

@app.get("/api/health")
def health_check():
    return {"status": "ok"}
