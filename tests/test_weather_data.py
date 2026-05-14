import unittest
from unittest.mock import patch, MagicMock
from germany_weather_map import weather_data
from germany_weather_map.weather_data import fetch_weather_matrix

class TestWeatherData(unittest.TestCase):
    
    def setUp(self):
        # Reset the global session before each test
        weather_data._session = None

    @patch('germany_weather_map.weather_data.requests_cache.CachedSession')
    def test_fetch_weather_matrix(self, mock_session_class):
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"current": {"precipitation": 0.5, "temperature_2m": 20.0, "weather_code": 1, "cloud_cover": 50}}
        mock_response.from_cache = False
        mock_session.get.return_value = mock_response
        
        with patch('time.sleep') as mock_sleep:
            grid = fetch_weather_matrix()
            self.assertTrue(mock_sleep.called)
            
        self.assertEqual(len(grid), 64)
        self.assertTrue(any(p["data"] is not None for row in grid for p in row if p["is_inside"]))

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
            self.assertFalse(mock_sleep.called)

    @patch('germany_weather_map.weather_data.requests_cache.CachedSession')
    def test_fetch_weather_matrix_cache_fallback(self, mock_session_class):
        mock_session_success = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"current": {"precipitation": 0, "temperature_2m": 20, "weather_code": 1, "cloud_cover": 0}}
        mock_session_success.get.return_value = mock_response
        
        # Fail first initialization, succeed second
        mock_session_class.side_effect = [Exception("Failed to load sqlite"), mock_session_success]
        
        with patch('time.sleep'):
            fetch_weather_matrix()
            
        self.assertEqual(mock_session_class.call_count, 2)
        # Second call should use 'memory' backend
        self.assertEqual(mock_session_class.call_args_list[1][1]['backend'], 'memory')

    @patch('germany_weather_map.weather_data.requests_cache.CachedSession')
    def test_fetch_weather_matrix_rate_limit(self, mock_session_class):
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        
        mock_response_429 = MagicMock()
        mock_response_429.status_code = 429
        mock_response_200 = MagicMock()
        mock_response_200.status_code = 200
        mock_response_200.json.return_value = {"current": {"precipitation": 0, "temperature_2m": 20, "weather_code": 1, "cloud_cover": 0}}
        mock_response_200.from_cache = True
        
        mock_session.get.side_effect = [mock_response_429, mock_response_200]
        
        with patch('time.sleep'):
            fetch_weather_matrix()
            
        self.assertTrue(mock_session.get.called)
        # Verify cache-only fallback was attempted
        self.assertTrue(mock_session.get.call_args[1].get('only_if_cached'))

if __name__ == "__main__":
    unittest.main()
