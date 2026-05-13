import unittest
import numpy as np
from germany_weather_map.map_utils import load_germany_boundary, lats, lons

class TestMapUtils(unittest.TestCase):
    def test_load_germany_boundary(self):
        boundary = load_germany_boundary()
        self.assertIsNotNone(boundary)
        # Check if it has the expected area or bounds roughly
        self.assertTrue(boundary.area > 0)
        
    def test_grid_dimensions(self):
        self.assertEqual(len(lats), 64)
        self.assertEqual(len(lons), 32)
        
    def test_lat_lon_ranges(self):
        # LAT_MIN, LAT_MAX = 47.3, 55.0
        # LON_MIN, LON_MAX = 5.9, 15.0
        self.assertTrue(np.min(lats) < 48)
        self.assertTrue(np.max(lats) > 54)
        self.assertTrue(np.min(lons) < 7)
        self.assertTrue(np.max(lons) > 14)

if __name__ == "__main__":
    unittest.main()
