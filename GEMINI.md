# Gemini Project Instructions

This file contains foundational mandates for AI agents working on the `germany-weather-map` project. These instructions take absolute precedence over general defaults.

## Project Structure & Architecture
- `src/germany_weather_map/`: Root package for the application.
    - `main.py`: CLI Entry point. Handles argument parsing, logging setup (with `-v/--verbose` for debug), legend toggle (`-l/--legend`), and binary output (`-o/--output`). Keep logic minimal.
    - `weather_data.py`: Data Acquisition Layer. Handles API interactions, caching, and batching logic. Supports `fast_mode` for serverless environments.
    - `display.py`: Presentation Layer. Completely decoupled from the CLI. Contains functions to generate RGB framebuffers and save them to binary files or render them to the terminal.
    - `map_utils.py`: Geospatial Utilities. Manages the coordinate grid and boundary checks using `germany.json`.
- `api/`: Vercel Serverless Function entry point.
    - `index.py`: FastAPI application serving processed weather maps via `/api/weather`.
- `tests/`: Test suite mirroring the source structure.
    - `test_integration.py`: End-to-end CLI flow verification.
- `README.md`: High-level project overview and usage guide. Keep this updated with any major feature or architectural changes.
- `germany.json`: Critical GeoJSON data for country boundaries.
- `GEMINI.md`: AI project instructions and foundational mandates.
- `vercel.json`: Vercel deployment configuration.
- `notes/`: Detailed guides and recommendations.
    - `vercel_setup.md`: Step-by-step Vercel deployment instructions.
    - `hardware_recommendations.md`: Advice for ESP32 and LED matrix setup.

## Vercel Deployment & API
The application runs as a Vercel Serverless Function. See `notes/vercel_setup.md` for the full deployment walkthrough.

### Persistent Shared Cache
To prevent rate limits, the application supports **Vercel KV (Redis)**.
- It detects `KV_URL` or `REDIS_URL` environment variables automatically.
- All serverless instances share this cache, ensuring the API is only hit once every 15 minutes globally.

### Endpoints
- **HTML Preview:** `GET /` or `GET /api/preview` (Defaults to **Precipitation**)
    - Explicit paths: `/api/preview/precip`, `/api/preview/temp`, `/api/preview/cloud`.
- **Binary Data:** `GET /api/weather` (Defaults to **Precipitation**)
    - Explicit paths: `/api/weather/precip`, `/api/weather/temp`, `/api/weather/cloud`.
- **Health Check:** `GET /api/health`

## Engineering Standards
- **Testing Requirements:** Every code change must be accompanied by corresponding unit and/or integration tests.
- **Coverage Goal:** Maintain a minimum of 90% code coverage.
    - Run tests: `export PYTHONPATH=$PYTHONPATH:$(pwd)/src && python3 -m unittest discover tests`
    - Run coverage: `coverage run -m unittest discover tests && coverage report`
- **Logging over Printing:** Always use the standard `logging` module for status updates and error reporting. Use `self.assertLogs` in tests to keep output clean.
- **Module Execution:** Run as a module: `python3 -m germany_weather_map.main`.

## Technical Context
- **API:** Uses Open-Meteo DWD ICON API.
- **Data Dir:** Project root contains `germany.json`, which is required for boundary calculations.
- **Dependencies:** Managed via `requirements.txt` and `pyproject.toml`.
