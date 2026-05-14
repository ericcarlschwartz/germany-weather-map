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
# Do not cache incomplete/errored responses
NO_CACHE_HEADER = {"Cache-Control": "no-store, max-age=0"}

def handle_map_request(map_type: str, response_format: str = "html"):
    data, is_complete = fetch_weather_matrix(fast_mode=True, cache_backend='memory')
    fb = create_framebuffer(data, map_type=map_type)
    headers = CACHE_HEADER if is_complete else NO_CACHE_HEADER
    
    if response_format == "html":
        html_content = render_map_to_html(data, fb, map_type=map_type)
        return HTMLResponse(content=html_content, headers=headers)
    else:
        return Response(content=fb.tobytes(), media_type="application/octet-stream", headers=headers)

# --- Preview Endpoints (HTML) ---

@app.get("/", response_class=HTMLResponse)
@app.get("/api/preview", response_class=HTMLResponse)
def preview_default():
    return handle_map_request(map_type="precip", response_format="html")

@app.get("/api/preview/precip", response_class=HTMLResponse)
def preview_precip():
    return handle_map_request(map_type="precip", response_format="html")

@app.get("/api/preview/temp", response_class=HTMLResponse)
def preview_temp():
    return handle_map_request(map_type="temp", response_format="html")

@app.get("/api/preview/cloud", response_class=HTMLResponse)
def preview_cloud():
    return handle_map_request(map_type="cloud", response_format="html")

# --- Binary Endpoints (Octet-Stream) ---

@app.get("/api/weather")
def weather_default():
    return handle_map_request(map_type="precip", response_format="binary")

@app.get("/api/weather/precip")
def weather_precip():
    return handle_map_request(map_type="precip", response_format="binary")

@app.get("/api/weather/temp")
def weather_temp():
    return handle_map_request(map_type="temp", response_format="binary")

@app.get("/api/weather/cloud")
def weather_cloud():
    return handle_map_request(map_type="cloud", response_format="binary")

@app.get("/api/health")
def health_check():
    return {"status": "ok"}
