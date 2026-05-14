# Vercel Deployment Implementation Guide (for AI Agents)

This guide provides specific technical instructions for an AI agent to transition this project from a CLI tool to a Vercel Serverless Function, enabling the "Proxy Strategy" for hardware displays.

## 1. Context & Constraints
- **Target:** Vercel Python Runtime (Serverless).
- **Timeout:** Hobby tier has a **10-second limit**. Current CLI logic takes ~25s due to `time.sleep`.
- **Filesystem:** Read-only. `requests-cache` cannot use the default SQLite backend.
- **Dependencies:** `shapely` requires the `GEOS` C library. Vercel usually handles this, but binary wheels are preferred.

## 2. Required Refactors

### `weather_data.py`
- **Disable Sleep:** Add a `fast_mode=False` parameter to `fetch_weather_matrix`. If `True`, skip `time.sleep(2)`. Open-Meteo allows 600 requests/min, so for ~11 batches, we are well within limits.
- **Pluggable Cache:** Modify the `CachedSession` initialization to allow a `backend` override. 
    - For Vercel, use `'memory'`.
    - Ideally, implement an optional integration with **Vercel KV (Redis)** using the `requests-cache` Redis backend.

### `display.py`
- Ensure `render_map_to_terminal` remains decoupled. The API will only call `create_framebuffer`.

## 3. New Files Required

### `api/index.py` (The Entry Point)
Use **FastAPI** for its speed and native support for binary responses.
```python
from fastapi import FastAPI, Response
from germany_weather_map.weather_data import fetch_weather_matrix
from germany_weather_map.display import create_framebuffer

app = FastAPI()

@app.get("/api/weather")
def get_weather_binary(map_type: str = "temp"):
    data = fetch_weather_matrix(fast_mode=True)
    fb = create_framebuffer(data, map_type=map_type)
    return Response(content=fb.tobytes(), media_type="application/octet-stream")
```

### `vercel.json`
```json
{
  "rewrites": [{ "source": "/api/(.*)", "destination": "/api/index.py" }]
}
```

### `requirements.txt`
Add `fastapi` and `uvicorn`. Ensure `numpy` and `shapely` versions are pinned.

## 4. Execution Steps for the Agent
1. **Surgical Update to `weather_data.py`:** Add `fast_mode` and update session config to handle missing `.weather_cache` file gracefully (fallback to memory).
2. **Implement `api/index.py`:** Create the FastAPI wrapper.
3. **Verify Locally:** Test with `vercel dev` or by running the FastAPI app directly.
4. **Deploy:** Final validation on Vercel environment.
