# tests/test_reviews.py
import unittest
from unittest.mock import patch, MagicMock
from services.db_service import DatabaseService


class TestReviews(unittest.TestCase):
    def setUp(self):
        """Patch MongoClient so DatabaseService doesn't connect to real DB"""
        patcher = patch("services.db_service.MongoClient", autospec=True)
        self.addCleanup(patcher.stop)
        self.mock_client_class = patcher.start()

        # Mock instance returned by MongoClient()
        self.mock_client_instance = MagicMock()
        self.mock_client_instance.admin.command.return_value = {"ok": 1}
        self.mock_client_class.return_value = self.mock_client_instance

        # Create service (uses mocked MongoClient)
        self.db_service = DatabaseService()
        self.db_service.db = MagicMock()

    
    def test_get_reviews_by_place(self):
        mock_reviews = [
            {"_id": "123", "place_id": "place_1", "author": "Ali", "rating": 5},
            {"_id": "124", "place_id": "place_1", "author": "Sara", "rating": 4}
        ]
        self.db_service.db.reviews.find.return_value = mock_reviews

        reviews = self.db_service.get_reviews_by_place("place_1")
        self.assertEqual(len(reviews), 2)
        self.assertEqual(reviews[0]["author"], "Ali")


    @patch("services.db_service.datetime")
    def test_add_review(self, mock_datetime):
        mock_datetime.utcnow.return_value = "2025-09-04T10:00:00Z"
        mock_insert = MagicMock(inserted_id="fake_id")
        self.db_service.db.reviews.insert_one.return_value = mock_insert

        review_doc = {
            "place_id": "place_1",
            "author": "Ali",
            "rating": 5,
            "text": "Good place"
        }
        review_id = self.db_service.add_review(review_doc)

        self.assertEqual(review_id, "fake_id")
        self.db_service.db.reviews.insert_one.assert_called_once()

    @patch("services.db_service.ObjectId", side_effect=lambda x: x)  # ✅ bypass validation
    def test_delete_review_success(self, mock_oid):
        mock_delete = MagicMock(deleted_count=1)
        self.db_service.db.reviews.delete_one.return_value = mock_delete

        result = self.db_service.delete_review("fake_review_id")
        self.assertTrue(result)

    @patch("services.db_service.ObjectId", side_effect=lambda x: x)  # ✅ bypass validation
    def test_delete_review_failure(self, mock_oid):
        mock_delete = MagicMock(deleted_count=0)
        self.db_service.db.reviews.delete_one.return_value = mock_delete

        result = self.db_service.delete_review("fake_review_id")
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
