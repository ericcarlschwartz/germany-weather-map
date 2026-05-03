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

    def test_get_temp_color_extremely_cold(self):
        # < -5 (Dark Blue: 21)
        self.assertIn("\033[48;5;21m", get_temp_color(-10))
        self.assertIn("\033[48;5;21m", get_temp_color(-5.1))

    def test_get_temp_color_freezing(self):
        # < 0 (Blue: 33)
        self.assertIn("\033[48;5;33m", get_temp_color(-5))
        self.assertIn("\033[48;5;33m", get_temp_color(-0.1))

    def test_get_temp_color_cold(self):
        # < 7 (Cyan: 45)
        self.assertIn("\033[48;5;45m", get_temp_color(0))
        self.assertIn("\033[48;5;45m", get_temp_color(6.9))

    def test_get_temp_color_cool(self):
        # < 14 (Green: 40)
        self.assertIn("\033[48;5;40m", get_temp_color(7))
        self.assertIn("\033[48;5;40m", get_temp_color(13.9))

    def test_get_temp_color_mild(self):
        # < 21 (Light Green: 118)
        self.assertIn("\033[48;5;118m", get_temp_color(14))
        self.assertIn("\033[48;5;118m", get_temp_color(20.9))

    def test_get_temp_color_warm(self):
        # < 28 (Yellow: 226)
        self.assertIn("\033[48;5;226m", get_temp_color(21))
        self.assertIn("\033[48;5;226m", get_temp_color(27.9))

    def test_get_temp_color_hot(self):
        # < 35 (Orange: 214)
        self.assertIn("\033[48;5;214m", get_temp_color(28))
        self.assertIn("\033[48;5;214m", get_temp_color(34.9))

    def test_get_temp_color_extremely_hot(self):
        # 35+ (Red: 196)
        self.assertIn("\033[48;5;196m", get_temp_color(35))
        self.assertIn("\033[48;5;196m", get_temp_color(45))

if __name__ == "__main__":
    unittest.main()
