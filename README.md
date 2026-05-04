# Germany Weather Map

A simple Python application that fetches weather data from Open-Meteo (DWD ICON-D2 Model) and displays a dot matrix map of Germany.

## Installation

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    cd germany-weather-map
    ```

2.  Install dependencies:
    ```bash
    pip install .
    ```

## Usage

You can run the application using the `weather-map` command (after installation) or directly via Python:

```bash
# Default: Temperature Map
weather-map

# Explicit Temperature Map
weather-map temp

# Precipitation Map
weather-map precip
```

Or using python:
```bash
python src/germany_weather_map/main.py temp
python src/germany_weather_map/main.py precip
```

## Features

- Fetches real-time temperature or precipitation data for a grid across Germany.
- Visualizes weather data in a simple text-based matrix format with color scales.
- Supports both Temperature and Precipitation maps.

## Development

- **Source Code:** Located in `src/germany_weather_map/`
- **Tests:** Located in `tests/`
- **Run Tests:**
  ```bash
  export PYTHONPATH=./src && python3 tests/test_display.py
  ```
