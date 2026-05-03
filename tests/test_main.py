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

    def test_get_temp_color_12tempera(self):
        # Test each of the 12 bins in the 12Tempera scheme
        ranges = [
            (-15, "\033[48;5;57m"),   # < -10
            (-8,  "\033[48;5;63m"),   # < -5
            (-2,  "\033[48;5;33m"),   # < 0
            (2,   "\033[48;5;39m"),   # < 5
            (7,   "\033[48;5;45m"),   # < 10
            (12,  "\033[48;5;40m"),   # < 15
            (17,  "\033[48;5;118m"),  # < 20
            (22,  "\033[48;5;226m"),  # < 25
            (27,  "\033[48;5;220m"),  # < 30
            (32,  "\033[48;5;214m"),  # < 35
            (37,  "\033[48;5;202m"),  # < 40
            (45,  "\033[48;5;196m"),  # 40+
        ]
        for temp, expected_color in ranges:
            with self.subTest(temp=temp):
                self.assertIn(expected_color, get_temp_color(temp))

if __name__ == "__main__":
    unittest.main()
