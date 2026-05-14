import unittest
import numpy as np
from germany_weather_map.display import (
    get_precip_rgb, get_temp_rgb, get_cloud_rgb, 
    is_border, create_framebuffer
)

class TestWeatherMap(unittest.TestCase):
    def test_get_precip_rgb(self):
        self.assertEqual(get_precip_rgb(0), (50, 50, 50))
        self.assertEqual(get_precip_rgb(0.1), (0, 255, 255)) # Cyan
        self.assertEqual(get_precip_rgb(100.0), (255, 0, 255)) # Magenta

    def test_get_temp_rgb(self):
        self.assertEqual(get_temp_rgb(-15), (95, 0, 215))
        self.assertEqual(get_temp_rgb(45), (255, 0, 0))

    def test_get_cloud_rgb(self):
        self.assertEqual(get_cloud_rgb(5), (0, 255, 255))
        self.assertEqual(get_cloud_rgb(95), (255, 255, 255))

    def test_create_framebuffer(self):
        # 3x3 grid to ensure center is inside, and we have distinct outside vs border
        # [ O O O ]
        # [ O I O ]
        # [ O O O ]
        weather_data = [
            [{"is_inside": False}, {"is_inside": False}, {"is_inside": False}],
            [{"is_inside": False}, {"is_inside": True, "data": {"current": {"temperature_2m": 20.0, "precipitation": 0.0, "cloud_cover": 0}}}, {"is_inside": False}],
            [{"is_inside": False}, {"is_inside": False}, {"is_inside": False}]
        ]
        fb = create_framebuffer(weather_data, "temp")
        self.assertEqual(fb.shape, (3, 3, 3))
        
        # Center point with 20C
        self.assertEqual(tuple(fb[1, 1]), get_temp_rgb(20))
        # Top-left corner (0,0) is a border because it's adjacent to (1,1)
        self.assertEqual(tuple(fb[0, 0]), (200, 200, 200)) # COLOR_BORDER


if __name__ == "__main__":
    unittest.main()
