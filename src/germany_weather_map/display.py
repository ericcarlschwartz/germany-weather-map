import numpy as np

# RGB Color Constants
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_BORDER = (200, 200, 200)  # Light gray for border
COLOR_OUTSIDE = (20, 20, 20)    # Very dark gray for outside
COLOR_MISSING = (255, 0, 255)   # Magenta for missing data '?'

def get_precip_rgb(precip):
    if precip <= 0:
        return (50, 50, 50)  # Dark gray for 0mm
    if precip < 0.5:
        return (0, 255, 255)    # Cyan
    if precip < 2.0:
        return (0, 0, 255)      # Blue
    if precip < 5.0:
        return (0, 255, 0)      # Green
    if precip < 10.0:
        return (255, 255, 0)    # Yellow
    if precip < 20.0:
        return (255, 0, 0)      # Red
    return (255, 0, 255)        # Magenta

def get_temp_rgb(temp):
    if temp < -10: return (95, 0, 215)
    if temp < -5:  return (95, 95, 255)
    if temp < 0:   return (0, 135, 255)
    if temp < 5:   return (0, 175, 255)
    if temp < 10:  return (0, 215, 255)
    if temp < 15:  return (0, 215, 0)
    if temp < 20:  return (135, 255, 0)
    if temp < 25:  return (255, 255, 0)
    if temp < 30:  return (255, 215, 0)
    if temp < 35:  return (255, 175, 0)
    if temp < 40:  return (255, 95, 0)
    return (255, 0, 0)

def get_cloud_rgb(cloud_cover):
    if cloud_cover < 10: return (0, 255, 255)   # Cyan (Clear)
    if cloud_cover < 30: return (220, 220, 220) # Very Light Gray
    if cloud_cover < 60: return (180, 180, 180) # Light Gray
    if cloud_cover < 80: return (100, 100, 100) # Gray
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
    # Create an empty RGB framebuffer (uint8)
    fb = np.zeros((rows, cols, 3), dtype=np.uint8)

    for r in range(rows):
        for c in range(cols):
            point = weather_data[r][c]
            if is_border(weather_data, r, c):
                fb[r, c] = COLOR_BORDER
            elif not point["is_inside"]:
                fb[r, c] = COLOR_OUTSIDE
            elif point["data"]:
                if map_type == "precip":
                    val = point['data']['current']['precipitation']
                    fb[r, c] = get_precip_rgb(val)
                elif map_type == "cloud":
                    val = point['data']['current']['cloud_cover']
                    fb[r, c] = get_cloud_rgb(val)
                else: # temp
                    val = point['data']['current']['temperature_2m']
                    fb[r, c] = get_temp_rgb(val)
            else:
                fb[r, c] = COLOR_MISSING
    return fb

def rgb_to_ansi(rgb):
    """Convert an RGB tuple to a 24-bit ANSI background escape code."""
    r, g, b = rgb
    return f"\033[48;2;{r};{g};{b}m   \033[0m"

def render_map(weather_data, map_type="temp"):
    fb = create_framebuffer(weather_data, map_type)
    
    if map_type == "precip":
        print("\n--- Germany Precipitation Map ---")
    elif map_type == "cloud":
        print("\n--- Germany Cloud Cover Map ---")
    else:
        print("\n--- Germany Temperature Map ---")
    
    for r in range(fb.shape[0]):
        line = ""
        for c in range(fb.shape[1]):
            rgb = fb[r, c]
            # Use specific characters for borders/outside to match previous style
            point = weather_data[r][c]
            if is_border(weather_data, r, c):
                line += rgb_to_ansi(rgb)
            elif not point["is_inside"]:
                line += " x  "
            elif not point["data"]:
                line += " ?  "
            else:
                line += rgb_to_ansi(rgb)
        print(line)
