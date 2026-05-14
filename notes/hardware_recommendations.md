# Hardware & Future Development Notes

This document summarizes the hardware recommendations and architectural decisions made to support the transition from a terminal application to a physical LED weather map.

## Recommended Hardware
For a dedicated "always-on" bookshelf display, the **ESP32** pathway is recommended for its stability and low power consumption.

### The "Gold Standard" Setup
- **Controller:** [Adafruit Matrix Portal S3](https://www.adafruit.com/product/5778) (ESP32-S3). Plugs directly into the panel.
- **Display:** [64x32 RGB LED Matrix](https://www.adafruit.com/product/2276) (4mm or 5mm pitch). Matches the 64x32 code grid perfectly.
- **Aesthetics:** [Black LED Diffusion Acrylic](https://www.adafruit.com/product/4594). Essential for a professional, "pixelated" look.
- **Power:** 5V 4A (or 10A) power supply with a 2.1mm DC jack.

## Software Architecture (Hardware-Ready)
The codebase has been refactored to decouple data generation from display rendering:
- **Data Layer (`weather_data.py`):** Fetches and caches weather data with a fallback to stale data on API rate limits.
- **Logic Layer (`create_framebuffer`):** Generates a raw NumPy RGB array (the "framebuffer").
- **Output Layer:**
    - **Terminal:** Renders the framebuffer using 256-color ANSI.
    - **Binary (`--output`):** Exports the raw 6144 bytes ($64 \times 32 \times 3$) for hardware use.

## Implementation Strategies
When you return to the project, consider these two paths for the hardware:

### 1. The "Proxy" Strategy (Recommended for ESP32)
Since an ESP32 is too constrained to run complex Python libraries like `shapely` or `numpy`:
1. Run this Python application on a local server (Raspberry Pi, PC, or cheap VPS).
2. Use a simple script to run the map every 15 minutes and save it as a binary file.
3. Serve that binary file over a simple HTTP endpoint.
4. Program the ESP32 (in CircuitPython) to simply download the bytes and "blast" them to the screen.

### 2. The "Direct Drive" Strategy (Raspberry Pi)
If using a Raspberry Pi as the controller:
1. Install the `rpi-rgb-led-matrix` library.
2. Use the existing Python code directly.
3. Write a new driver in `display.py` that loops through the NumPy framebuffer and calls `matrix.SetPixel()`.

## Project Status Highlights
- **Coverage:** 92% (Unit + Integration tests).
- **API Resilience:** Automatically switches to "cache-only" mode if rate-limited.
- **Formatting:** Fixed rectangular grid alignment in the terminal for accurate previews.
