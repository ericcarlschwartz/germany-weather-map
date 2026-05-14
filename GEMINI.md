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
- `germany.json`: Critical GeoJSON data for country boundaries.
- `vercel.json`: Vercel deployment configuration.

## Vercel Deployment & API
The application is configured to run as a Vercel Serverless Function using the Python runtime.

### Endpoints
- **HTML Preview:** `GET /` or `GET /api/preview` (Defaults to **Precipitation**)
    - Explicit paths: `/api/preview/precip`, `/api/preview/temp`, `/api/preview/cloud`.
    - Renders a high-fidelity CSS-based grid for browser testing.
- **Binary Data:** `GET /api/weather` (Defaults to **Precipitation**)
    - Explicit paths: `/api/weather/precip`, `/api/weather/temp`, `/api/weather/cloud`.
    - Returns raw RGB bytes ($64 \times 32 \times 3 = 6144$ bytes) for hardware consumption.
- **Health Check:** `GET /api/health`

### Performance & Caching
- **Edge Cache:** Responses include `Cache-Control: s-maxage=900, stale-while-revalidate=300`. Vercel will cache the processed map for 15 minutes.
- **Fast Mode:** The API calls `fetch_weather_matrix(fast_mode=True)` to skip internal `time.sleep` calls, ensuring execution stays under the 10s serverless timeout.
- **Batching:** Uses a batch size of 500 coordinates per request to balance between API efficiency and URI length limits (avoiding 414 errors).

## Documentation Maintenance Mandate
- **Proactive Updates:** Whenever a new feature, CLI argument, or architectural change is implemented, you MUST update the `README.md` and any other relevant documentation immediately. Do not wait for a specific request from the user to do so.
- **Sync Validation:** Before concluding a task, verify that the `README.md` accurately reflects the current state of the application's features, installation steps, and usage examples.

## Engineering Standards
- **Testing Requirements:** Every code change must be accompanied by corresponding unit and/or integration tests.
- **Coverage Goal:** Maintain a minimum of 90% code coverage. Run `coverage report` after changes to ensure this threshold is met.
- **Logging over Printing:** Always use the standard `logging` module for status updates and error reporting. Reserved `print` for actual map output intended for the user.
- **Module Execution:** The application is designed to be run as a module (`python3 -m germany_weather_map.main`). Ensure all package-relative imports are maintained.

## Technical Context
- **API:** Uses Open-Meteo DWD ICON API.
- **Data Dir:** Project root contains `germany.json`, which is required for boundary calculations.
- **Dependencies:** Managed via `requirements.txt` and `pyproject.toml`.
