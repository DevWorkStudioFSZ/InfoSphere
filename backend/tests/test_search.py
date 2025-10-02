# tests/test_search.py
import unittest
from unittest.mock import patch
from flask import Flask
from routes.search import router as search_router


class TestSearchRoute(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config["TESTING"] = True
        self.app.config["DEBUG"] = True
        self.app.register_blueprint(search_router)
        self.client = self.app.test_client()

    def test_missing_city_or_category(self):
        response = self.client.post("/search", json={"city": "Lahore"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    @patch("routes.search.search_places")
    def test_search_success(self, mock_search_places):
        mock_result = {
            "search_meta": {"city": "Lahore", "category": "libraries"},
            "entities": [{"name": "Punjab Public Library", "rating_average": 4.5}],
        }
        mock_search_places.return_value = mock_result

        response = self.client.post(
            "/search",
            json={"city": "Lahore", "category": "libraries", "filters": {"min_rating": 4}},
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("entities", data)
        self.assertEqual(data["entities"][0]["name"], "Punjab Public Library")

    @patch("routes.search.search_places", side_effect=Exception("API failure"))
    def test_search_api_failure(self, mock_search_places):
        response = self.client.post(
            "/search",
            json={"city": "Karachi", "category": "coffee shops"},
        )
        self.assertEqual(response.status_code, 500)
        data = response.get_json()
        self.assertEqual(data["error"], "API failure")

    @patch("routes.search.search_places")
    def test_filter_min_rating(self, mock_search_places):
        mock_result = {
            "search_meta": {"city": "Lahore", "category": "cafes"},
            "entities": [
                {"name": "Low Rated Cafe", "rating_average": 2.5},
                {"name": "High Rated Cafe", "rating_average": 4.7},
            ],
        }
        mock_search_places.return_value = mock_result

        response = self.client.post(
            "/search",
            json={"city": "Lahore", "category": "cafes", "filters": {"min_rating": 4}},
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        names = [e["name"] for e in data["entities"]]
        self.assertIn("High Rated Cafe", names)
        self.assertNotIn("Low Rated Cafe", names)

    @patch("routes.search.search_places")
    def test_filter_has_phone(self, mock_search_places):
        mock_result = {
            "search_meta": {"city": "Lahore", "category": "shops"},
            "entities": [
                {"name": "Shop With Phone", "phone": "+123"},
                {"name": "Shop Without Phone", "phone": None},
            ],
        }
        mock_search_places.return_value = mock_result

        response = self.client.post(
            "/search",
            json={"city": "Lahore", "category": "shops", "filters": {"has_phone": True}},
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        names = [e["name"] for e in data["entities"]]
        self.assertIn("Shop With Phone", names)
        self.assertNotIn("Shop Without Phone", names)


if __name__ == "__main__":
    unittest.main()
