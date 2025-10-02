# tests/test_google_places.py
import unittest
from unittest.mock import patch, MagicMock
from services import google_places


class TestGooglePlaces(unittest.TestCase):

    def test_build_query_valid(self):
        q = google_places._build_query("lahore", "restaurants")
        self.assertIn("amenity", q)
        self.assertIn("restaurant", q)

    def test_build_query_invalid_category(self):
        with self.assertRaises(ValueError):
            google_places._build_query("lahore", "invalid_cat")

    def test_build_query_invalid_city(self):
        with self.assertRaises(ValueError):
            google_places._build_query("unknowncity", "restaurants")

    def test_best_phone(self):
        tags = {"contact:phone": "12345"}
        self.assertEqual(google_places._best_phone(tags), "12345")

    def test_best_website(self):
        tags = {"website": "https://example.com"}
        self.assertEqual(google_places._best_website(tags), "https://example.com")

    def test_compose_address(self):
        tags = {
            "addr:housenumber": "42",
            "addr:street": "Main St",
            "addr:city": "Lahore"
        }
        addr = google_places._compose_address(tags)
        self.assertEqual(addr, "42, Main St, Lahore")

    @patch("services.google_places.requests.post")
    def test_post_overpass_success(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"elements": []}
        mock_post.return_value = mock_resp

        q = google_places._build_query("lahore", "restaurants")
        data = google_places._post_overpass(q)
        self.assertEqual(data, {"elements": []})

    @patch("services.google_places.requests.post", side_effect=Exception("Network error"))
    def test_post_overpass_fail(self, mock_post):
        q = google_places._build_query("lahore", "restaurants")
        # Expect the raw Exception, since _post_overpass doesn't wrap it
        with self.assertRaises(Exception) as ctx:
            google_places._post_overpass(q, max_retries=1, pause=0)
        self.assertIn("Network error", str(ctx.exception))


    @patch("services.google_places.get_db")
    @patch("services.google_places._post_overpass")
    @patch("services.google_places._build_query")
    def test_search_places_with_cache(self, mock_build, mock_post, mock_get_db):
        mock_db = MagicMock()
        mock_db.get_cached_search.return_value = {
            "timestamp": "2025-09-08T00:00:00",
            "entities": [{"name": "Test Place"}]
        }
        mock_get_db.return_value = mock_db

        result = google_places.search_places("lahore", "restaurants")
        self.assertTrue(result["search_meta"]["cached"])
        self.assertEqual(result["entities"][0]["name"], "Test Place")

    @patch("services.google_places.get_db")
    @patch("services.google_places._post_overpass")
    @patch("services.google_places._build_query")
    def test_search_places_no_cache(self, mock_build, mock_post, mock_get_db):
        mock_build.return_value = "query"
        mock_post.return_value = {
            "elements": [
                {
                    "type": "node",
                    "id": 1,
                    "tags": {"name": "New Place"},
                    "center": {"lat": 31.5204, "lon": 74.3587},
                }
            ]
        }

        mock_db = MagicMock()
        mock_db.get_cached_search.return_value = None
        mock_get_db.return_value = mock_db

        result = google_places.search_places("lahore", "restaurants")

        self.assertFalse(result["search_meta"]["cached"])
        self.assertEqual(result["entities"][0]["name"], "New Place")
        mock_db.save_place_data.assert_called()
        mock_db.cache_search_result.assert_called()
        mock_db.log_search_request.assert_called()


if __name__ == "__main__":
    unittest.main()
