# Hardware & Future Development Notes (EU Edition)

This document summarizes the hardware recommendations and architectural decisions made to support the transition from a terminal application to a physical LED weather map, with a focus on European suppliers.

## Recommended Hardware (European Sources)
For a dedicated "always-on" bookshelf display, the **ESP32** pathway is the official strategy.

### 1. The Controller: Adafruit Matrix Portal S3
This is the "brain" that plugs directly into the back of the LED panel.
- **BerryBase (DE):** [Adafruit Matrix Portal S3](https://www.berrybase.de/adafruit-matrixportal-s3-circuitpython-powered-internet-display)
- **Eckstein (DE):** [Adafruit Matrix Portal S3](https://eckstein-shop.de/Adafruit-MatrixPortal-S3-CircuitPython-Powered-Internet-Display)
- **Pimoroni (UK/EU):** [Matrix Portal S3](https://shop.pimoroni.com/products/adafruit-matrixportal-s3)

### 2. The Display: 64x32 RGB LED Matrix
Standard HUB75 panels. Matches our 64x32 code grid.
- **4mm Pitch (approx. 25.6 x 12.8 cm):** 
    - [BerryBase Option](https://www.berrybase.de/64x32-rgb-led-matrix-panel-4mm-pitch)
- **5mm Pitch (approx. 32.0 x 16.0 cm - better for larger shelves):**
    - [Eckstein Option](https://eckstein-shop.de/64x32-RGB-LED-Matrix-Panel-5mm-pitch)

### 3. The Look: Diffusion
Raw LEDs are harsh; diffusion makes them look like professional "pixels."
- **Black Acrylic:** Look for "Plexiglas GS Schwarz 9H01" (usually 3mm). Many EU sellers on eBay or Etsy offer custom laser-cutting to the exact size of your 64x32 panel.
- **Alternative:** [Pimoroni 3mm Black Acrylic Sheet](https://shop.pimoroni.com/products/black-acrylic-sheet-210mm-x-297mm-x-3mm).

### 4. Power Supply
You need a 5V supply with enough current (Amps).
- **Recommendation:** 5V / 4A (20W) or 5V / 10A (50W) power supply with a 2.1mm DC jack.
- **Source:** [BerryBase 5V 4A Power Supply](https://www.berrybase.de/steckernetzteil-5v-4a-20w-hohlstecker-5-5mm/2-1mm).

---

## Enclosure & Framing Options
To make the map look like a finished product rather than a project, consider these framing paths:

### 1. The "IKEA Hack" (Shadow Box)
- **Frame:** IKEA **SANNAHED** (25x25cm, black).
- **Setup:** Create a custom black mount board (Passepartout) with a rectangular window for the matrix. Sandwich the diffusion sheet between the glass and the matrix.
- **Pros:** Very professional look, hides all cables and the controller inside the frame.

### 2. The Minimalist Acrylic Case
- **Design:** Order custom laser-cut rectangles (e.g., from **Formulor** in DE) slightly larger than the matrix.
- **Setup:** Use **M3 Standoffs** (approx 30mm) to bolt a black front sheet and a clear back sheet together, trapping the matrix in the middle.
- **Pros:** Extremely sleek and modern, "floating" appearance.

### 3. The 3D-Printed Frame
- **Design:** Use the community-standard [Matrix Portal 64x32 Case](https://www.printables.com/model/161474-64x32-rgb-led-matrix-case-for-adafruit-matrix-port).
- **Refinement:** Print in **Matte Black PLA** and lightly sand for a high-end plastic finish.

### Pro Tips for a Polished Look
- **90-Degree Adapters:** Use a 90-degree USB-C or DC barrel jack adapter so the cable drops straight down, allowing the frame to sit flush against a wall.
- **Light Sensor:** The Matrix Portal S3 has a built-in light sensor. You can use it in your final code to dim the LEDs automatically when your room lights are off.
- **Blackout Tape:** If light leaks from the sides of the frame, use black electrical tape or "LightDims" to seal the edges behind the diffusion sheet.

---

## Software Architecture (Hardware-Ready)
The codebase has been refactored to decouple data generation from display rendering:
- **Data Layer (`weather_data.py`):** Fetches/caches weather data with fallback to stale data.
- **Logic Layer (`create_framebuffer`):** Generates a raw NumPy RGB array.
- **Vercel API:** Serves raw RGB bytes via `/api/weather` and HTML preview via `/api/preview`.

## Implementation Strategy: The "Proxy" Strategy
The "Proxy" strategy is the implemented path for this project:
1. The **Vercel API** does the heavy lifting (Shapely, NumPy, API batching).
2. The **ESP32** (Matrix Portal S3) runs a simple CircuitPython script.
3. It fetches the binary data from `https://your-site.com/api/weather/precip`.
4. It reads the 6144 bytes and updates the matrix.

## Project Status Highlights
- **Coverage:** 93% (Unit + Integration tests).
- **API Resilience:** 500-point batching (avoids 414 errors) + Vercel Edge Caching.
- **Visualization:** Consistent 12Tempera color scheme across Terminal, Browser, and Binary formats.
