def get_precip_color(precip):
    if precip <= 0:
        return " .  "
    
    # ANSI background colors for radar-like visualization
    if precip < 0.5:
        color = "\033[46m"  # Cyan: Light rain
    elif precip < 2.0:
        color = "\033[44m"  # Blue: Moderate rain
    elif precip < 5.0:
        color = "\033[42m"  # Green: Heavy rain
    elif precip < 10.0:
        color = "\033[43m"  # Yellow: Very heavy rain
    elif precip < 20.0:
        color = "\033[41m"  # Red: Intense rain
    else:
        color = "\033[45m"  # Magenta: Extreme rain
        
    return f"{color}   \033[0m "

def get_temp_color(temp):
    # 12Tempera Color Scheme (Smoothed 12-bin transition)
    # Mapping based on typical meteorological transitions: Purple -> Blue -> Cyan -> Green -> Yellow -> Orange -> Red
    if temp < -10:
        color = "\033[48;5;57m"   # Deep Purple
    elif temp < -5:
        color = "\033[48;5;63m"   # Purple-Blue
    elif temp < 0:
        color = "\033[48;5;33m"   # Blue
    elif temp < 5:
        color = "\033[48;5;39m"   # Light Blue
    elif temp < 10:
        color = "\033[48;5;45m"   # Cyan
    elif temp < 15:
        color = "\033[48;5;40m"   # Green
    elif temp < 20:
        color = "\033[48;5;118m"  # Light Green
    elif temp < 25:
        color = "\033[48;5;226m"  # Yellow
    elif temp < 30:
        color = "\033[48;5;220m"  # Gold / Dark Yellow
    elif temp < 35:
        color = "\033[48;5;214m"  # Orange
    elif temp < 40:
        color = "\033[48;5;202m"  # Orange-Red
    else:
        color = "\033[48;5;196m"  # Bright Red

    return f"{color}   \033[0m "

def is_border(grid, r, c):
    # A point is a border if it's currently 'outside' but has at least one 'inside' neighbor
    if grid[r][c]["is_inside"]:
        return False
    
    rows = len(grid)
    cols = len(grid[0])
    
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr][nc]["is_inside"]:
                    return True
    return False

BORDER_COLOR = "\033[47m   \033[0m "

def render_map(weather_data, map_type="temp"):
    if map_type == "precip":
        print("\n--- Germany Precipitation Doppler Radar ---")
        print(" Legend: \033[46m   \033[0m <0.5mm, \033[44m   \033[0m <2mm, \033[42m   \033[0m <5mm, \033[43m   \033[0m <10mm, \033[41m   \033[0m <20mm, \033[45m   \033[0m 20mm+")
        print(" (x = outside boundary, . = 0mm, white = border) \n")
        
        for r, row in enumerate(weather_data):
            line = ""
            for c, point in enumerate(row):
                if is_border(weather_data, r, c):
                    line += BORDER_COLOR
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
                    line += BORDER_COLOR
                elif not point["is_inside"]:
                    line += " x  "
                elif point["data"]:
                    temp = point['data']['current']['temperature_2m']
                    line += get_temp_color(temp)
                else:
                    line += " ?  " 
            print(line)
