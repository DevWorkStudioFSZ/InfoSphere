
import unittest
from unittest.mock import patch
import json

from app import create_app

class ExportRouteTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    @patch("routes.export.search_places")
    def test_export_json_success(self, mock_search):
        mock_search.return_value = [
            {
                "name": "Test Library",
                "address": "123 Street, Lahore",
                "lat": 31.5,
                "lng": 74.3,
                "phone": "12345",
                "website": "http://example.com",
                "hours": "Mo-Fr 09:00-18:00",
                "rating_average": 4.5,
                "rating_count": 12,
                "source_url": "https://osm.org/node/1",
                "raw_tags": {}
            }
        ]

        response = self.client.get("/api/export?city=Lahore&category=libraries&format=json")
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertIn("export_meta", data)
        self.assertIn("entities", data)
        self.assertEqual(data["export_meta"]["format"], "json")

    @patch("routes.export.search_places")
    def test_export_csv_success(self, mock_search):
        mock_search.return_value = [
            {
                "name": "Test Restaurant",
                "address": "456 Street, Lahore",
                "lat": 31.6,
                "lng": 74.35,
                "phone": None,
                "website": None,
                "hours": None,
                "rating_average": None,
                "rating_count": None,
                "source_url": "https://osm.org/node/2",
                "raw_tags": {}
            }
        ]

        response = self.client.get("/api/export?city=Lahore&category=restaurants&format=csv")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "text/csv")
        self.assertIn("Test Restaurant", response.data.decode())

    def test_export_missing_params(self):
        response = self.client.get("/api/export?format=json")
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)

    def test_export_invalid_format(self):
        response = self.client.get("/api/export?city=Lahore&category=libraries&format=xml")
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)


if __name__ == "__main__":
    unittest.main()
