# tests/test_geocode.py
import unittest
from unittest.mock import patch, MagicMock
from services import geocode

class TestGeocode(unittest.TestCase):
    def setUp(self):
        self.address = "Lahore, Pakistan"

    #Successful geocode
    @patch("services.geocode.requests.get")
    def test_geocode_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "OK",
            "results": [
                {
                    "formatted_address": "Lahore, Pakistan",
                    "geometry": {"location": {"lat": 31.5497, "lng": 74.3436}}
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = geocode.geocode_address(self.address)

        self.assertIsNotNone(result)
        self.assertEqual(result["formatted_address"], "Lahore, Pakistan")
        self.assertAlmostEqual(result["lat"], 31.5497)
        self.assertAlmostEqual(result["lng"], 74.3436)

    #No results found
    @patch("services.geocode.requests.get")
    def test_geocode_no_results(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "ZERO_RESULTS", "results": []}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = geocode.geocode_address(self.address)
        self.assertIsNone(result)

    #Request error (e.g. network issue)
    @patch("services.geocode.requests.get", side_effect=Exception("Network error"))
    def test_geocode_request_error(self, mock_get):
        result = geocode.geocode_address(self.address)
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()
