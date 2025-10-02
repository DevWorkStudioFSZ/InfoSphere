import os
import certifi
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("MONGODB_URI")
print("🔗 Using URI:", uri)

try:
    client = MongoClient(uri, tlsCAFile=certifi.where())
    dbs = client.list_database_names()
    print("✅ Connected! Databases:", dbs)
except Exception as e:
    print("❌ Failed to connect:", e)
