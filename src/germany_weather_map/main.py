import argparse
import logging

from .weather_data import fetch_weather_matrix
from .display import render_map

def main():
    parser = argparse.ArgumentParser(description="Germany Weather Map")
    parser.add_argument(
        "map_type", 
        choices=["temp", "precip"], 
        nargs="?", 
        default="temp",
        help="Type of map to display: 'temp' for temperature or 'precip' for precipitation (default: temp)"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    args = parser.parse_args()

    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=log_level, format='%(message)s')

    try:
        weather_data = fetch_weather_matrix()
        if not weather_data:
            logging.error("Failed to fetch weather data.")
            return

        render_map(weather_data, map_type=args.map_type)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
