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
                "weather_code": 1,
                "cloud_cover": 50
            }
        }
        mock_response.from_cache = False
        mock_session.get.return_value = mock_response
        
        # We need to mock time.sleep to speed up tests
        with patch('time.sleep') as mock_sleep:
            grid = fetch_weather_matrix()
            # Default fast_mode=False, so sleep should be called
            self.assertTrue(mock_sleep.called)
            
        self.assertEqual(len(grid), 64)
        self.assertEqual(len(grid[0]), 32)
        
        # Check if some points have data
        has_data = False
        for row in grid:
            for point in row:
                if point["is_inside"] and point["data"] is not None:
                    has_data = True
                    break
        self.assertTrue(has_data)

    @patch('germany_weather_map.weather_data.requests_cache.CachedSession')
    def test_fetch_weather_matrix_fast_mode(self, mock_session_class):
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"current": {"precipitation": 0, "temperature_2m": 20, "weather_code": 1, "cloud_cover": 0}}
        mock_response.from_cache = False
        mock_session.get.return_value = mock_response

        with patch('time.sleep') as mock_sleep:
            fetch_weather_matrix(fast_mode=True)
            # fast_mode=True, so sleep should NOT be called
            self.assertFalse(mock_sleep.called)

    @patch('germany_weather_map.weather_data.requests_cache.CachedSession')
    def test_fetch_weather_matrix_cache_fallback(self, mock_session_class):
        # First call fails, second call (fallback to memory) succeeds
        mock_session_class.side_effect = [Exception("Failed to load sqlite"), MagicMock()]
        
        with patch('time.sleep'):
            fetch_weather_matrix()
            
        self.assertEqual(mock_session_class.call_count, 2)
        self.assertEqual(mock_session_class.call_args_list[1][1]['backend'], 'memory')

if __name__ == "__main__":
    unittest.main()
