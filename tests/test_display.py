import unittest
import numpy as np
import os
from germany_weather_map.display import (
    get_precip_rgb, get_temp_rgb, get_cloud_rgb, 
    is_border, create_framebuffer, save_binary_framebuffer,
    render_map_to_html
)

class TestWeatherMap(unittest.TestCase):
    def test_get_precip_rgb(self):
        self.assertEqual(get_precip_rgb(0), (60, 60, 60))
        self.assertEqual(get_precip_rgb(0.1), (0, 255, 255)) # Cyan
        self.assertEqual(get_precip_rgb(25.0), (255, 0, 0)) # Red

    def test_get_temp_rgb(self):
        self.assertEqual(get_temp_rgb(-15), (128, 0, 128))
        self.assertEqual(get_temp_rgb(45), (128, 0, 0))

    def test_get_cloud_rgb(self):
        self.assertEqual(get_cloud_rgb(5), (0, 255, 255))
        self.assertEqual(get_cloud_rgb(95), (255, 255, 255))

    def test_create_framebuffer(self):
        # 3x3 grid
        weather_data = [
            [{"is_inside": False}, {"is_inside": False}, {"is_inside": False}],
            [{"is_inside": False}, {"is_inside": True, "data": {"current": {"temperature_2m": 20.0, "precipitation": 0.0, "cloud_cover": 0}}}, {"is_inside": False}],
            [{"is_inside": False}, {"is_inside": False}, {"is_inside": False}]
        ]
        fb = create_framebuffer(weather_data, "temp")
        self.assertEqual(fb.shape, (3, 3, 3))
        self.assertEqual(tuple(fb[1, 1]), get_temp_rgb(20))

    def test_save_binary_framebuffer(self):
        fb = np.zeros((2, 2, 3), dtype=np.uint8)
        fb[0, 0] = (255, 0, 0)
        path = "test_fb.bin"
        try:
            success = save_binary_framebuffer(fb, path)
            self.assertTrue(success)
            self.assertTrue(os.path.exists(path))
            self.assertEqual(os.path.getsize(path), 2 * 2 * 3)
            with open(path, "rb") as f:
                data = f.read()
                self.assertEqual(data[0], 255)
        finally:
            if os.path.exists(path):
                os.remove(path)

    def test_render_map_to_html(self):
        weather_data = [[{"is_inside": True, "data": {"current": {"temperature_2m": 20.0, "precipitation": 0.0, "cloud_cover": 0}}}]]
        fb = create_framebuffer(weather_data, "temp")
        html = render_map_to_html(weather_data, fb, "temp")
        self.assertIn("<html>", html)
        self.assertIn("rgb(255,255,0)", html) # Yellow color for 20C
        self.assertIn("Germany Weather Map", html)

if __name__ == "__main__":
    unittest.main()
