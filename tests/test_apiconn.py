import unittest
from unittest import TestCase
from unittest.mock import patch

import api_connection


class TestAPIData(TestCase):

    # Verify that get_lat_lon is parsing lat/long values from geocode response
    @patch('api_connection.get_API_data')
    def test_location_to_lat_lon(self, mock_response_data):
        mock_lat = 1234
        mock_lon = 5678
        example_api_response = {'results': [{'geometry': {'lat': mock_lat, 'lon': mock_lon}}]}

        mock_response_data.side_effect = [ example_api_response ]
        
        coords = api_connection.get_lat_lon('testloc')
        self.assertEqual(1234, coords['lat'])
        self.assertEqual(5678, coords['lon'])

if __name__ == '__main__':
    unittest.main()