import unittest
from germany_weather_map.main import get_precip_color, get_temp_color

class TestWeatherMap(unittest.TestCase):
    def test_get_precip_color_zero(self):
        self.assertEqual(get_precip_color(0), " .  ")
        self.assertEqual(get_precip_color(-1), " .  ")

    def test_get_precip_color_light(self):
        # < 0.5mm (Cyan)
        self.assertIn("\033[46m", get_precip_color(0.1))
        self.assertIn("\033[46m", get_precip_color(0.4))

    def test_get_precip_color_moderate(self):
        # < 2.0mm (Blue)
        self.assertIn("\033[44m", get_precip_color(0.5))
        self.assertIn("\033[44m", get_precip_color(1.9))

    def test_get_precip_color_heavy(self):
        # < 5.0mm (Green)
        self.assertIn("\033[42m", get_precip_color(2.0))
        self.assertIn("\033[42m", get_precip_color(4.9))

    def test_get_precip_color_very_heavy(self):
        # < 10.0mm (Yellow)
        self.assertIn("\033[43m", get_precip_color(5.0))
        self.assertIn("\033[43m", get_precip_color(9.9))

    def test_get_precip_color_intense(self):
        # < 20.0mm (Red)
        self.assertIn("\033[41m", get_precip_color(10.0))
        self.assertIn("\033[41m", get_precip_color(19.9))

    def test_get_precip_color_extreme(self):
        # 20.0mm+ (Magenta)
        self.assertIn("\033[45m", get_precip_color(20.0))
        self.assertIn("\033[45m", get_precip_color(100.0))

    def test_get_temp_color_freezing(self):
        # < 0 (White)
        self.assertIn("\033[47m", get_temp_color(-5))
        self.assertIn("\033[47m", get_temp_color(-0.1))

    def test_get_temp_color_cold(self):
        # < 10 (Blue)
        self.assertIn("\033[44m", get_temp_color(0))
        self.assertIn("\033[44m", get_temp_color(9.9))

    def test_get_temp_color_cool(self):
        # < 18 (Cyan)
        self.assertIn("\033[46m", get_temp_color(10))
        self.assertIn("\033[46m", get_temp_color(17.9))

    def test_get_temp_color_mild(self):
        # < 25 (Green)
        self.assertIn("\033[42m", get_temp_color(18))
        self.assertIn("\033[42m", get_temp_color(24.9))

    def test_get_temp_color_warm(self):
        # < 30 (Yellow)
        self.assertIn("\033[43m", get_temp_color(25))
        self.assertIn("\033[43m", get_temp_color(29.9))

    def test_get_temp_color_hot(self):
        # < 35 (Red)
        self.assertIn("\033[41m", get_temp_color(30))
        self.assertIn("\033[41m", get_temp_color(34.9))

    def test_get_temp_color_very_hot(self):
        # 35+ (Magenta)
        self.assertIn("\033[45m", get_temp_color(35))
        self.assertIn("\033[45m", get_temp_color(40))

if __name__ == "__main__":
    unittest.main()
