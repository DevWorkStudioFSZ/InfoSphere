import unittest
import json
import csv
from io import StringIO
from datetime import datetime
from zoneinfo import ZoneInfo

from data import schema, normalizer, exporter, filters


class TestSchema(unittest.TestCase):
    def test_normalize_phone(self):
        self.assertEqual(schema.normalize_phone("+1 (234) 567-8900"), "+12345678900")
        self.assertIsNone(schema.normalize_phone(""))

    def test_normalize_website(self):
        self.assertTrue(schema.normalize_website("example.com").startswith("http://"))
        self.assertIn("example.com", schema.normalize_website("https://example.com?x=1#frag"))

    def test_normalize_address(self):
        self.assertEqual(schema.normalize_address(" 123,Main St  "), "123, Main St")

    def test_compute_entity_id_stable(self):
        id1 = schema.compute_entity_id("Shop", "123 St", "Lahore", None)
        id2 = schema.compute_entity_id("Shop", "123 St", "Lahore", None)
        self.assertEqual(id1, id2)

    def test_entity_to_from_mongo(self):
        e = schema.Entity(
            id="abc",
            name="Test Shop",
            category="books",
            address="123 Street",
            city="Lahore",
            lat=1.23,
            lng=4.56,
            phone="+123",
            website="http://example.com",
            hours={"mon": [("09:00", "17:00")]},
            rating_average=4.5,
            rating_count=10,
            source="google",
            source_id="gid",
            source_url="http://maps",
            open_now=True,
            created_at="2024-01-01T00:00:00Z",
            updated_at="2024-01-01T00:00:00Z",
        )
        mongo_doc = e.to_mongo()
        e2 = schema.Entity.from_mongo(mongo_doc)
        self.assertEqual(e.id, e2.id)
        self.assertEqual(e.name, e2.name)


class TestNormalizer(unittest.TestCase):
    def make_entity(self, **kwargs):
        return schema.Entity(
            id=kwargs.get("id", "id1"),
            name=kwargs.get("name", "Cafe One"),
            category=kwargs.get("category", "cafe"),
            address=kwargs.get("address", "123 Street"),
            city=kwargs.get("city", "Lahore"),
            lat=kwargs.get("lat", 31.5),
            lng=kwargs.get("lng", 74.3),
            phone=kwargs.get("phone", None),
            website=kwargs.get("website", None),
            hours=kwargs.get("hours", None),
            rating_average=kwargs.get("rating_average", 4.0),
            rating_count=kwargs.get("rating_count", 10),
            source="google",
            source_id=kwargs.get("source_id", None),
            source_url=kwargs.get("source_url", None),
            open_now=kwargs.get("open_now", None),
            created_at="2024-01-01T00:00:00Z",
            updated_at="2024-01-01T00:00:00Z",
        )

    def test_dedupe_by_phone(self):
        e1 = self.make_entity(id="1", phone="+111")
        e2 = self.make_entity(id="2", phone="+111")
        merged, stats = normalizer.dedupe_entities([e1, e2])
        self.assertEqual(len(merged), 1)
        self.assertEqual(stats["deduped"], 1)

    def test_dedupe_by_site(self):
        e1 = self.make_entity(id="1", website="http://x.com")
        e2 = self.make_entity(id="2", website="http://x.com")
        merged, _ = normalizer.dedupe_entities([e1, e2])
        self.assertEqual(len(merged), 1)

    def test_dedupe_by_name_and_distance(self):
        e1 = self.make_entity(id="1", name="Cafe A", lat=31.5000, lng=74.3000)
        e2 = self.make_entity(id="2", name="Cafe A", lat=31.5005, lng=74.3005)
        merged, _ = normalizer.dedupe_entities([e1, e2])
        self.assertEqual(len(merged), 1)

    def test_merge_cluster_prefers_highest_rating_count(self):
        e1 = self.make_entity(id="1", rating_count=5, rating_average=4.1)
        e2 = self.make_entity(id="2", rating_count=50, rating_average=3.9)
        merged = normalizer.merge_cluster([e1, e2])
        self.assertEqual(merged.id, "2")  # picked higher rating_count


class TestExporter(unittest.TestCase):
    def setUp(self):
        self.entities = [
            schema.Entity(
                id="1",
                name="Test Cafe",
                category="cafe",
                address="123 Street",
                city="Lahore",
                lat=31.5,
                lng=74.3,
                phone="+123",
                website="http://example.com",
                hours={"mon": [("09:00", "17:00")]},
                rating_average=4.5,
                rating_count=10,
                source="google",
                source_id="gid",
                source_url="http://maps",
                open_now=True,
                created_at="2024-01-01T00:00:00Z",
                updated_at="2024-01-01T00:00:00Z",
            )
        ]
        self.meta = {"city": "Lahore", "category": "cafes"}

    def test_export_json(self):
        data = exporter.export_json(self.entities, self.meta)
        decoded = json.loads(data.decode("utf-8"))
        self.assertIn("search_meta", decoded)
        self.assertIn("entities", decoded)

    def test_export_csv_and_headers(self):
        data = exporter.export_csv(self.entities)
        text = data.decode("utf-8")
        reader = csv.DictReader(StringIO(text))
        rows = list(reader)
        self.assertEqual(rows[0]["name"], "Test Cafe")

    def test_export_response_json(self):
        filename, data, mimetype = exporter.export_response("json", self.entities, self.meta)
        self.assertEqual(filename, "results.json")
        self.assertIn("application/json", mimetype)

    def test_export_response_csv(self):
        filename, data, mimetype = exporter.export_response("csv", self.entities, self.meta)
        self.assertEqual(filename, "results.csv")
        self.assertIn("text/csv", mimetype)

    def test_export_response_invalid_format(self):
        with self.assertRaises(ValueError):
            exporter.export_response("xml", self.entities, self.meta)


class TestFilters(unittest.TestCase):
    def make_entity(self, **kwargs):
        return schema.Entity(
            id=kwargs.get("id", "id1"),
            name=kwargs.get("name", "Cafe Test"),
            category=kwargs.get("category", "cafe"),
            address=kwargs.get("address", "123 Street"),
            city=kwargs.get("city", "Lahore"),
            lat=kwargs.get("lat", 31.5),
            lng=kwargs.get("lng", 74.3),
            phone=kwargs.get("phone"),
            website=kwargs.get("website"),
            hours=kwargs.get("hours"),
            rating_average=kwargs.get("rating_average", 4.0),
            rating_count=kwargs.get("rating_count", 10),
            source="google",
            source_id=kwargs.get("source_id", None),
            source_url=kwargs.get("source_url", None),
            open_now=kwargs.get("open_now", None),
            created_at="2024-01-01T00:00:00Z",
            updated_at="2024-01-01T00:00:00Z",
        )

    def test_is_open_now_true(self):
        dt = datetime(2024, 1, 1, 10, 0, tzinfo=ZoneInfo("Asia/Karachi"))  # Monday 10:00
        e = self.make_entity(hours={"mon": [("09:00", "17:00")]})
        self.assertTrue(filters.is_open_now(e, when=dt))

    def test_is_open_now_false(self):
        dt = datetime(2024, 1, 1, 20, 0, tzinfo=ZoneInfo("Asia/Karachi"))  # Monday 20:00
        e = self.make_entity(hours={"mon": [("09:00", "17:00")]})
        self.assertFalse(filters.is_open_now(e, when=dt))

    def test_apply_filters_min_rating(self):
        e1 = self.make_entity(rating_average=2.0)
        e2 = self.make_entity(rating_average=4.5)
        out = filters.apply_filters([e1, e2], min_rating=3.0)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0].rating_average, 4.5)

    def test_apply_filters_phone_and_website(self):
        e1 = self.make_entity(phone=None, website=None)
        e2 = self.make_entity(phone="+111", website="http://x.com")
        out = filters.apply_filters([e1, e2], has_phone=True, has_website=True)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0].id, "id1" if e1.phone else "id1" if e2.phone else "id2")


if __name__ == "__main__":
    unittest.main()
