import unittest
from unittest.mock import patch, MagicMock
from germany_weather_map.weather_data import fetch_weather_matrix

class TestWeatherData(unittest.TestCase):
    
    @patch('germany_weather_map.weather_data.requests_cache.CachedSession')
    def test_fetch_weather_matrix(self, mock_session_class):
        # Setup mock session and response
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "current": {
                "precipitation": 0.5,
                "temperature_2m": 20.0,
                "weather_code": 1
            }
        }
        mock_response.from_cache = False
        mock_session.get.return_value = mock_response
        
        # We need to mock time.sleep to speed up tests
        with patch('time.sleep'):
            grid = fetch_weather_matrix()
            
        self.assertEqual(len(grid), 64)
        self.assertEqual(len(grid[0]), 32)
        
        # Check if some points have data
        # Note: only points inside Germany will have data fetched
        has_data = False
        for row in grid:
            for point in row:
                if point["is_inside"] and point["data"] is not None:
                    has_data = True
                    break
        self.assertTrue(has_data)

if __name__ == "__main__":
    unittest.main()
