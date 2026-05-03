import argparse

from weather_data import fetch_weather_matrix
from display import get_precip_color, get_temp_color, is_border

def main():
    parser = argparse.ArgumentParser(description="Germany Weather Map")
    parser.add_argument(
        "map_type", 
        choices=["temp", "precip"], 
        nargs="?", 
        default="temp",
        help="Type of map to display: 'temp' for temperature or 'precip' for precipitation (default: temp)"
    )
    args = parser.parse_args()

    weather_data = fetch_weather_matrix()
    if not weather_data:
        return

    border_color = "\033[47m   \033[0m "

    if args.map_type == "precip":
        print("\n--- Germany Precipitation Doppler Radar ---")
        print(" Legend: \033[46m   \033[0m <0.5mm, \033[44m   \033[0m <2mm, \033[42m   \033[0m <5mm, \033[43m   \033[0m <10mm, \033[41m   \033[0m <20mm, \033[45m   \033[0m 20mm+")
        print(" (x = outside boundary, . = 0mm, white = border) \n")
        
        for r, row in enumerate(weather_data):
            line = ""
            for c, point in enumerate(row):
                if is_border(weather_data, r, c):
                    line += border_color
                elif not point["is_inside"]:
                    line += " x  "
                elif point["data"]:
                    precip = point['data']['current']['precipitation']
                    line += get_precip_color(precip)
                else:
                    line += " ?  " 
            print(line)
    else:
        print("\n--- Germany Temperature Map (12Tempera) ---")
        print(" Legend: \033[48;5;57m   \033[0m <-10°C, \033[48;5;63m   \033[0m <-5°C, \033[48;5;33m   \033[0m <0°C, \033[48;5;39m   \033[0m <5°C, \033[48;5;45m   \033[0m <10°C, \033[48;5;40m   \033[0m <15°C,")
        print("         \033[48;5;118m   \033[0m <20°C, \033[48;5;226m   \033[0m <25°C, \033[48;5;220m   \033[0m <30°C, \033[48;5;214m   \033[0m <35°C, \033[48;5;202m   \033[0m <40°C, \033[48;5;196m   \033[0m 40°C+")
        print(" (x = outside boundary, white = border) \n")
        
        for r, row in enumerate(weather_data):
            line = ""
            for c, point in enumerate(row):
                if is_border(weather_data, r, c):
                    line += border_color
                elif not point["is_inside"]:
                    line += " x  "
                elif point["data"]:
                    temp = point['data']['current']['temperature_2m']
                    line += get_temp_color(temp)
                else:
                    line += " ?  " 
            print(line)

if __name__ == "__main__":
    main()
