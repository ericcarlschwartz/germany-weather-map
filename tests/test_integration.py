import unittest
from unittest.mock import patch, MagicMock
import io
import os
from contextlib import redirect_stdout
from germany_weather_map.main import main

class TestIntegration(unittest.TestCase):
    
    @patch('germany_weather_map.main.fetch_weather_matrix')
    def test_main_temp(self, mock_fetch):
        mock_fetch.return_value = [[{"is_inside": False} for _ in range(5)] for _ in range(5)]
        mock_fetch.return_value[2][2] = {"is_inside": True, "data": {"current": {"temperature_2m": 20.0, "precipitation": 0.0, "cloud_cover": 0}}}
        
        with patch('sys.argv', ['weather-map', 'temp']):
            f = io.StringIO()
            with redirect_stdout(f):
                main()
            output = f.getvalue()
            
        self.assertIn("Germany Temperature Map", output)
        self.assertIn("x", output)
        
    @patch('germany_weather_map.main.fetch_weather_matrix')
    def test_main_precip(self, mock_fetch):
        mock_fetch.return_value = [[{"is_inside": True, "data": {"current": {"temperature_2m": 20.0, "precipitation": 0.5, "cloud_cover": 50}}}]]
        with patch('sys.argv', ['weather-map', 'precip']):
            f = io.StringIO()
            with redirect_stdout(f):
                main()
            output = f.getvalue()
        self.assertIn("Germany Precipitation Map", output)

    @patch('germany_weather_map.main.fetch_weather_matrix')
    def test_main_cloud(self, mock_fetch):
        mock_fetch.return_value = [[{"is_inside": True, "data": {"current": {"temperature_2m": 20.0, "precipitation": 0.5, "cloud_cover": 90}}}]]
        with patch('sys.argv', ['weather-map', 'cloud']):
            f = io.StringIO()
            with redirect_stdout(f):
                main()
            output = f.getvalue()
        self.assertIn("Germany Cloud Cover Map", output)

    @patch('germany_weather_map.main.fetch_weather_matrix')
    def test_main_verbose(self, mock_fetch):
        mock_fetch.return_value = [[{"is_inside": True, "data": {"current": {"temperature_2m": 20.0, "precipitation": 0.5, "cloud_cover": 0}}}]]
        with patch('sys.argv', ['weather-map', 'temp', '-v']):
            with redirect_stdout(io.StringIO()):
                main()

    @patch('germany_weather_map.main.fetch_weather_matrix')
    def test_main_legend(self, mock_fetch):
        mock_fetch.return_value = [[{"is_inside": True, "data": {"current": {"temperature_2m": 20.0, "precipitation": 0.5, "cloud_cover": 0}}}]]
        with patch('sys.argv', ['weather-map', 'temp', '--legend']):
            f = io.StringIO()
            with redirect_stdout(f):
                main()
            output = f.getvalue()
        self.assertIn("Legend:", output)

    @patch('germany_weather_map.main.fetch_weather_matrix')
    def test_main_binary_output(self, mock_fetch):
        mock_fetch.return_value = [[{"is_inside": True, "data": {"current": {"temperature_2m": 20.0, "precipitation": 0.0, "cloud_cover": 0}}}]]
        path = "integration_test.bin"
        try:
            with patch('sys.argv', ['weather-map', 'temp', '--output', path]):
                with redirect_stdout(io.StringIO()):
                    main()
            self.assertTrue(os.path.exists(path))
            self.assertEqual(os.path.getsize(path), 1 * 1 * 3)
        finally:
            if os.path.exists(path):
                os.remove(path)

if __name__ == "__main__":
    unittest.main()
