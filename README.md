# Germany Weather Map

A Python application and API for visualizing weather data across Germany on a grid. Designed for both high-level terminal visualization and low-level hardware integration (e.g., ESP32 LED matrices).

## Features

- **Multi-Layer Visualization**: Supports Temperature, Precipitation, and Cloud Cover maps.
- **CLI Interface**: Render maps directly in your terminal with optional legends.
- **Binary Output**: Generate raw 24-bit RGB framebuffers for hardware drivers.
- **Serverless API**: FastAPI-based endpoints for HTML previews and binary data retrieval.
- **Smart Caching**: Built-in support for local file caching and Vercel KV (Redis) to prevent API rate limiting.
- **Geospatial Logic**: Accurate mapping of weather data to a grid using GeoJSON boundaries.

## Getting Started

### Prerequisites

- Python 3.8+
- [Optional] Redis (for persistent shared caching)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/germany-weather-map.git
   cd germany-weather-map
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install the package in editable mode:**
   ```bash
   pip install -e .
   ```

## Usage

### CLI

The application can be run as a module or via the `weather-map` entry point.

```bash
# Display temperature map with legend
weather-map temp --legend

# Display precipitation map in verbose mode
weather-map precip -v

# Save a cloud cover binary framebuffer to a file
weather-map cloud -o weather_frame.bin
```

### API

The API is designed to run as a serverless function. To run it locally:

```bash
uvicorn api.index:app --reload
```

**Key Endpoints:**
- `GET /api/preview`: HTML visualization of the weather map.
- `GET /api/weather`: Raw binary framebuffer for hardware consumption.
- `GET /api/health`: Service health check.

## Documentation

- [Vercel Deployment Guide](notes/vercel_setup.md): Detailed instructions for hosting on Vercel.
- [Hardware Recommendations](notes/hardware_recommendations.md): Advice for ESP32 and LED matrix integration.

## Development

### Testing

Tests are located in the `tests/` directory and mirror the source structure.

```bash
# Run all tests
python3 -m unittest discover tests

# Run tests with coverage
coverage run -m unittest discover tests
coverage report
```

### Project Structure

- `src/germany_weather_map/`: Core logic (data acquisition, display, geospatial utils).
- `api/`: FastAPI entry point for serverless deployment.
- `germany.json`: GeoJSON data for Germany's boundaries.
- `tests/`: Comprehensive test suite.

## License

[Specify License if applicable]
