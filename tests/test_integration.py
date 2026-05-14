import unittest
from unittest.mock import patch, MagicMock
import io
from contextlib import redirect_stdout
from germany_weather_map.main import main

class TestIntegration(unittest.TestCase):
    
    @patch('germany_weather_map.main.fetch_weather_matrix')
    def test_main_temp(self, mock_fetch):
        # 4x4 grid to have at least one point that is NOT a border and NOT inside
        # B B B B
        # B I I B
        # B B B B
        # B B B B
        # Wait, even a 4x4 might have all outside points as borders if (1,1) and (1,2) are inside.
        # Let's make it 5x5 and put (2,2) as inside.
        mock_fetch.return_value = [
            [{"is_inside": False} for _ in range(5)] for _ in range(5)
        ]
        mock_fetch.return_value[2][2] = {"is_inside": True, "data": {"current": {"temperature_2m": 20.0, "precipitation": 0.0, "cloud_cover": 0}}}
        
        with patch('sys.argv', ['weather-map', 'temp']):
            f = io.StringIO()
            with redirect_stdout(f):
                main()
            output = f.getvalue()
            
        self.assertIn("Germany Temperature Map", output)
        self.assertIn("x", output) # Outside boundary (point 0,0 is far from 2,2)
        
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
            
        self.assertIn("Germany Precipitation Map", output)

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

    @patch('germany_weather_map.main.fetch_weather_matrix')
    def test_main_legend(self, mock_fetch):
        mock_fetch.return_value = [
            [{"is_inside": True, "data": {"current": {"temperature_2m": 20.0, "precipitation": 0.5, "cloud_cover": 0}}}]
        ]
        
        with patch('sys.argv', ['weather-map', 'temp', '--legend']):
            f = io.StringIO()
            with redirect_stdout(f):
                main()
            output = f.getvalue()
            
        self.assertIn("Legend:", output)

if __name__ == "__main__":
    unittest.main()
