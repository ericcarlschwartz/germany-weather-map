import argparse
import logging

from .weather_data import fetch_weather_matrix
from .display import create_framebuffer, render_map_to_terminal, save_binary_framebuffer

def main():
    parser = argparse.ArgumentParser(description="Germany Weather Map")
    parser.add_argument(
        "map_type", 
        choices=["temp", "precip", "cloud"], 
        nargs="?", 
        default="temp",
        help="Type of map to display: 'temp', 'precip', or 'cloud' (default: temp)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show verbose output (debug messages)"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help=argparse.SUPPRESS
    )
    parser.add_argument(
        "-l", "--legend",
        action="store_true",
        help="Show map legend"
    )
    parser.add_argument(
        "-o", "--output",
        help="Path to save binary framebuffer output"
    )
    args = parser.parse_args()

    log_level = logging.DEBUG if (args.debug or args.verbose) else logging.INFO
    logging.basicConfig(level=log_level, format='%(message)s')

    try:
        weather_data = fetch_weather_matrix()
        if not weather_data:
            logging.error("Failed to fetch weather data.")
            return

        # 1. Create the hardware-ready framebuffer
        fb = create_framebuffer(weather_data, map_type=args.map_type)

        # 2. Handle outputs
        if args.output:
            save_binary_framebuffer(fb, args.output)
        else:
            render_map_to_terminal(weather_data, fb, map_type=args.map_type, show_legend=args.legend)

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
