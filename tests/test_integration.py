import unittest
from unittest.mock import patch, MagicMock
import io
from contextlib import redirect_stdout
from germany_weather_map.main import main

class TestIntegration(unittest.TestCase):
    
    @patch('germany_weather_map.main.fetch_weather_matrix')
    def test_main_temp(self, mock_fetch):
        # Create a tiny 2x2 grid for testing
        mock_fetch.return_value = [
            [
                {"is_inside": True, "data": {"current": {"temperature_2m": 20.0, "precipitation": 0.0, "cloud_cover": 0}}},
                {"is_inside": False, "data": None}
            ],
            [
                {"is_inside": False, "data": None},
                {"is_inside": True, "data": {"current": {"temperature_2m": 10.0, "precipitation": 1.0, "cloud_cover": 100}}}
            ]
        ]
        
        with patch('sys.argv', ['weather-map', 'temp']):
            f = io.StringIO()
            with redirect_stdout(f):
                main()
            output = f.getvalue()
            
        self.assertIn("Germany Temperature Map", output)
        self.assertIn("x", output) # Outside boundary
        
    @patch('germany_weather_map.main.fetch_weather_matrix')
    def test_main_precip(self, mock_fetch):
        mock_fetch.return_value = [
            [
                {"is_inside": True, "data": {"current": {"temperature_2m": 20.0, "precipitation": 0.5, "cloud_cover": 50}}},
                {"is_inside": False, "data": None}
            ]
        ]
        
        with patch('sys.argv', ['weather-map', 'precip']):
            f = io.StringIO()
            with redirect_stdout(f):
                main()
            output = f.getvalue()
            
        self.assertIn("Germany Precipitation Doppler Radar", output)

    @patch('germany_weather_map.main.fetch_weather_matrix')
    def test_main_cloud(self, mock_fetch):
        mock_fetch.return_value = [
            [
                {"is_inside": True, "data": {"current": {"temperature_2m": 20.0, "precipitation": 0.5, "cloud_cover": 90}}},
                {"is_inside": False, "data": None}
            ]
        ]
        
        with patch('sys.argv', ['weather-map', 'cloud']):
            f = io.StringIO()
            with redirect_stdout(f):
                main()
            output = f.getvalue()
            
        self.assertIn("Germany Cloud Cover Map", output)

    @patch('germany_weather_map.main.fetch_weather_matrix')
    def test_main_verbose(self, mock_fetch):
        mock_fetch.return_value = [
            [{"is_inside": True, "data": {"current": {"temperature_2m": 20.0, "precipitation": 0.5, "cloud_cover": 0}}}]
        ]
        
        # Test -v flag
        with patch('sys.argv', ['weather-map', 'temp', '-v']):
            with redirect_stdout(io.StringIO()):
                main()
        
        # Test --verbose flag
        with patch('sys.argv', ['weather-map', 'temp', '--verbose']):
            with redirect_stdout(io.StringIO()):
                main()

if __name__ == "__main__":
    unittest.main()
