from pymongo import MongoClient
from datetime import datetime, timedelta
from bson import ObjectId
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self):
        self.client = None
        self.db = None
        self.connect()
    
    def connect(self):
        """Connect to MongoDB Atlas"""
        try:
            mongodb_uri = os.getenv('MONGODB_URI')
            if not mongodb_uri or mongodb_uri.strip() == "":
                raise ValueError("MONGODB_URI is missing in environment variables")
            
            self.client = MongoClient(mongodb_uri)
            self.db = self.client['infosphere']
            self.client.admin.command('ping')
            logger.info("Connected to MongoDB Atlas successfully")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise  
    
    def is_connected(self):
        return self.db is not None
    
   #Cache methods
    def get_cached_search(self, cache_key):
        if self.db is None:
            raise RuntimeError("MongoDB not connected")
        try:
            one_hour_ago = datetime.utcnow() - timedelta(hours=1)
            cached = self.db.search_cache.find_one({
                'cache_key': cache_key,
                'created_at': {'$gte': one_hour_ago}
            })
            if cached:
                logger.info(f"Cache hit for key: {cache_key}")
                return {'entities': cached['entities'], 'timestamp': cached['timestamp']}
            return None
        except Exception as e:
            logger.error(f"Error retrieving cached search: {str(e)}")
            return None
    
    def cache_search_result(self, cache_key, result):
        if self.db is None:
            raise RuntimeError("MongoDB not connected")
        try:
            cache_doc = {
                'cache_key': cache_key,
                'entities': result['entities'],
                'timestamp': result['timestamp'],
                'search_params': result.get('search_params', {}),
                'created_at': datetime.utcnow(),
                'expires_at': datetime.utcnow() + timedelta(hours=1)
            }
            self.db.search_cache.replace_one({'cache_key': cache_key}, cache_doc, upsert=True)
            logger.info(f"Cached search result for key: {cache_key}")
        except Exception as e:
            logger.error(f"Error caching search result: {str(e)}")
    
    #Logging methods
    def log_search_request(self, city, category, ip_address, filters=None, results_count=0, response_time_ms=0):
        if self.db is None:
            raise RuntimeError("MongoDB not connected")
        try:
            log_doc = {
                'city': city,
                'category': category,
                'ip_address': ip_address,
                'filters_used': filters or {},
                'results_count': results_count,
                'response_time_ms': response_time_ms,
                'timestamp': datetime.utcnow()
            }
            self.db.search_logs.insert_one(log_doc)
            logger.info(f"Logged search: {city} - {category}")
        except Exception as e:
            logger.error(f"Error logging search request: {str(e)}")
    
    # Place data methods
    def save_place_data(self, place_data):
        if self.db is None:
            raise RuntimeError("MongoDB not connected")
        try:
            place_data['last_updated'] = datetime.utcnow()
            self.db.places_data.replace_one(
                {'place_id': place_data['place_id']},
                place_data,
                upsert=True
            )
            logger.info(f"Saved place data: {place_data.get('name', 'Unknown')}")
        except Exception as e:
            logger.error(f"Error saving place data: {str(e)}")
    
    # Review methods
    def get_reviews_by_place(self, place_id):
        """Fetch all reviews for a place"""
        if self.db is None:
            raise RuntimeError("MongoDB not connected")
        try:
            reviews = list(self.db.reviews.find({"place_id": place_id}))
            for r in reviews:
                r["_id"] = str(r["_id"])
            return reviews
        except Exception as e:
            logger.error(f"Error fetching reviews: {str(e)}")
            return []
    
    def add_review(self, review_doc):
        """Insert a new review"""
        if self.db is None:
            raise RuntimeError("MongoDB not connected")
        try:
            review_doc["created_at"] = datetime.utcnow()
            result = self.db.reviews.insert_one(review_doc)
            logger.info(f"Added review for place {review_doc['place_id']} by {review_doc['author']}")
            return result.inserted_id
        except Exception as e:
            logger.error(f"Error adding review: {str(e)}")
            raise
    
    def delete_review(self, review_id):
        """Delete review by ID"""
        if self.db is None:
            raise RuntimeError("MongoDB not connected")
        try:
            result = self.db.reviews.delete_one({"_id": ObjectId(review_id)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting review: {str(e)}")
            raise
