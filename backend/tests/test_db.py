import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from services.db_service import DatabaseService


class TestDatabaseService(unittest.TestCase):
    def setUp(self):
        """Patch MongoClient so no real DB is used"""
        patcher = patch("services.db_service.MongoClient")
        self.addCleanup(patcher.stop)
        self.mock_client = patcher.start()

        # Fake db with collection mocks
        self.mock_db = MagicMock()
        self.mock_client.return_value.__getitem__.return_value = self.mock_db
        self.mock_client.return_value.admin.command.return_value = {"ok": 1}

        # Service under test
        self.service = DatabaseService()
        self.service.db = self.mock_db

    #Connection
    def test_is_connected_true(self):
        self.assertTrue(self.service.is_connected())

    #Cache
    def test_get_cached_search_hit(self):
        one_hour_ago = datetime.utcnow() - timedelta(minutes=30)
        fake_cache = {"cache_key": "abc", "entities": [], "timestamp": "now", "created_at": one_hour_ago}
        self.mock_db.search_cache.find_one.return_value = fake_cache

        result = self.service.get_cached_search("abc")
        self.assertIn("entities", result)
        self.mock_db.search_cache.find_one.assert_called_once()

    def test_get_cached_search_miss(self):
        self.mock_db.search_cache.find_one.return_value = None
        result = self.service.get_cached_search("missing")
        self.assertIsNone(result)

    def test_cache_search_result(self):
        result = {"entities": [], "timestamp": "now"}
        self.service.cache_search_result("key123", result)
        self.mock_db.search_cache.replace_one.assert_called_once()

    #Search Logs
    def test_log_search_request(self):
        self.service.log_search_request("Lahore", "cafes", "127.0.0.1", {"min_rating": 4}, 5, 120)
        self.mock_db.search_logs.insert_one.assert_called_once()
        args, _ = self.mock_db.search_logs.insert_one.call_args
        self.assertEqual(args[0]["city"], "Lahore")

    #Places Data
    def test_save_place_data(self):
        place = {"place_id": "abc123", "name": "Test Cafe"}
        self.service.save_place_data(place)
        self.mock_db.places_data.replace_one.assert_called_once()
        
    #Reviews
    def test_get_reviews_by_place(self):
        self.mock_db.reviews.find.return_value = [{"_id": "oid1", "text": "ok"}]
        reviews = self.service.get_reviews_by_place("abc123")
        self.assertEqual(reviews[0]["text"], "ok")

    def test_add_review(self):
        mock_inserted = MagicMock(inserted_id="oid123")
        self.mock_db.reviews.insert_one.return_value = mock_inserted

        review = {"place_id": "abc123", "author": "Hanzala", "text": "Great!"}
        rid = self.service.add_review(review)

        self.assertEqual(rid, "oid123")
        self.mock_db.reviews.insert_one.assert_called_once()

    def test_delete_review(self):
        self.mock_db.reviews.delete_one.return_value.deleted_count = 1
        deleted = self.service.delete_review("507f1f77bcf86cd799439011")
        self.assertTrue(deleted)


if __name__ == "__main__":
    unittest.main()
