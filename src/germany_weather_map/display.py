import numpy as np

# RGB Color Constants
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_BORDER = (240, 240, 240)  # Very light gray/white for border
COLOR_OUTSIDE = (30, 30, 30)    # Dark gray for outside
COLOR_MISSING = (255, 0, 255)   # Magenta for missing data

def get_precip_rgb(precip):
    if precip <= 0:
        return (60, 60, 60)      # Dark gray for 0mm
    if precip < 0.5: return (0, 255, 255)    # Cyan
    if precip < 2.0: return (0, 0, 255)      # Blue
    if precip < 5.0: return (0, 255, 0)      # Green
    if precip < 10.0: return (255, 255, 0)   # Yellow
    if precip < 20.0: return (255, 128, 0)   # Orange
    return (255, 0, 0)                       # Red

def get_temp_rgb(temp):
    if temp < -10: return (128, 0, 128) # Purple
    if temp < -5:  return (0, 0, 255)   # Blue
    if temp < 0:   return (0, 128, 255) # Light Blue
    if temp < 5:   return (0, 255, 255) # Cyan
    if temp < 10:  return (0, 255, 128) # Teal
    if temp < 15:  return (0, 255, 0)   # Green
    if temp < 20:  return (128, 255, 0) # Lime
    if temp < 25:  return (255, 255, 0) # Yellow
    if temp < 30:  return (255, 128, 0) # Orange
    if temp < 35:  return (255, 64, 0)  # Deep Orange
    if temp < 40:  return (255, 0, 0)   # Red
    return (128, 0, 0)                  # Dark Red

def get_cloud_rgb(cloud_cover):
    if cloud_cover < 10: return (0, 255, 255)   # Cyan (Clear)
    if cloud_cover < 30: return (200, 200, 200) # Light Gray
    if cloud_cover < 60: return (140, 140, 140) # Gray
    if cloud_cover < 80: return (80, 80, 80)    # Dark Gray
    return (255, 255, 255)                      # White (Overcast)

def is_border(grid, r, c):
    if grid[r][c]["is_inside"]:
        return False
    rows = len(grid)
    cols = len(grid[0])
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0: continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr][nc]["is_inside"]:
                    return True
    return False

def create_framebuffer(weather_data, map_type="temp"):
    rows = len(weather_data)
    cols = len(weather_data[0])
    fb = np.zeros((rows, cols, 3), dtype=np.uint8)

    for r in range(rows):
        for c in range(cols):
            point = weather_data[r][c]
            if is_border(weather_data, r, c):
                fb[r, c] = COLOR_BORDER
            elif not point["is_inside"]:
                fb[r, c] = COLOR_OUTSIDE
            elif point["data"]:
                curr = point['data']['current']
                if map_type == "precip":
                    fb[r, c] = get_precip_rgb(curr['precipitation'])
                elif map_type == "cloud":
                    fb[r, c] = get_cloud_rgb(curr['cloud_cover'])
                else:
                    fb[r, c] = get_temp_rgb(curr['temperature_2m'])
            else:
                fb[r, c] = COLOR_MISSING
    return fb

def get_ansi_256_code(rgb):
    """Map RGB to the closest 256-color ANSI code."""
    r, g, b = rgb
    ri = int(r / 51)
    gi = int(g / 51)
    bi = int(b / 51)
    return 16 + 36 * ri + 6 * gi + bi

def rgb_to_ansi(rgb, char="   "):
    """Convert an RGB tuple to a 256-color ANSI background escape code."""
    code = get_ansi_256_code(rgb)
    return f"\033[48;5;{code}m{char}\033[0m"

def print_legend(map_type):
    print(" Legend:")
    if map_type == "precip":
        steps = [
            (0, "0mm"), (0.4, "<0.5mm"), (1.5, "<2mm"), 
            (4.0, "<5mm"), (9.0, "<10mm"), (15.0, "<20mm"), (25.0, "20mm+")
        ]
        line = " "
        for val, label in steps:
            line += rgb_to_ansi(get_precip_rgb(val)) + f" {label}  "
        print(line)
    elif map_type == "cloud":
        steps = [
            (5, "<10%"), (20, "<30%"), (50, "<60%"), (70, "<80%"), (90, "80%+")
        ]
        line = " "
        for val, label in steps:
            line += rgb_to_ansi(get_cloud_rgb(val)) + f" {label}  "
        print(line)
    else: # temp
        steps = [
            (-15, "<-10°C"), (-7, "<-5°C"), (-2, "<0°C"), (2, "<5°C"), 
            (7, "<10°C"), (12, "<15°C"), (17, "<20°C"), (22, "<25°C"), 
            (27, "<30°C"), (32, "<35°C"), (37, "<40°C"), (45, "40°C+")
        ]
        line = " "
        for i, (val, label) in enumerate(steps):
            line += rgb_to_ansi(get_temp_rgb(val)) + f" {label}  "
            if (i + 1) % 6 == 0: # Wrap legend for better terminal fit
                print(line)
                line = " "
        if line.strip():
            print(line)
    print(" (x = outside, white = border)\n")

def render_map(weather_data, map_type="temp", show_legend=False):
    fb = create_framebuffer(weather_data, map_type)
    
    titles = {
        "precip": "Germany Precipitation Map",
        "cloud": "Germany Cloud Cover Map",
        "temp": "Germany Temperature Map"
    }
    print(f"\n--- {titles.get(map_type, titles['temp'])} ---")
    
    if show_legend:
        print_legend(map_type)

    for r in range(fb.shape[0]):
        line = ""
        for c in range(fb.shape[1]):
            rgb = fb[r, c]
            point = weather_data[r][c]
            
            if is_border(weather_data, r, c):
                line += rgb_to_ansi(rgb, "   ") + " "
            elif not point["is_inside"]:
                line += " x  "
            elif not point["data"]:
                line += " ?  "
            else:
                line += rgb_to_ansi(rgb, "   ") + " "
        print(line)
