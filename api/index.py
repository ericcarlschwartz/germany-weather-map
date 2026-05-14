import os
import sys
from fastapi import FastAPI, Response

# Add src to path so we can import the package
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from germany_weather_map.weather_data import fetch_weather_matrix
from germany_weather_map.display import create_framebuffer

app = FastAPI()

@app.get("/api/weather")
def get_weather_binary(map_type: str = "temp"):
    # fast_mode=True to avoid Vercel timeout (10s limit)
    # cache_backend='memory' for read-only filesystem
    data = fetch_weather_matrix(fast_mode=True, cache_backend='memory')
    fb = create_framebuffer(data, map_type=map_type)
    return Response(content=fb.tobytes(), media_type="application/octet-stream")

@app.get("/api/health")
def health_check():
    return {"status": "ok"}
