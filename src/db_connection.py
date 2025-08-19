import os
import pymongo
from pymongo.errors import PyMongoError

class DbConnection:
    def __init__(self):
        self.collection_name = os.getenv("MONGODB_COLLECTION")

        try:
            mongo_user = os.getenv("MONGODB_USER")
            mongo_password = os.getenv("MONGODB_PASSWORD")
            mongo_db = os.getenv("MONGODB_DATABASE")
            mongo_host = os.getenv("MONGODB_HOST", "localhost")
            mongo_port = os.getenv("MONGODB_PORT", "27017")
            auth_db = os.getenv("MONGODB_AUTH_DB", "admin")

            self.client = pymongo.MongoClient(
                host=mongo_host,
                port=int(mongo_port),
                username=mongo_user,
                password=mongo_password,
                authSource=auth_db
            )

            self.db = self.client[mongo_db]
        except PyMongoError as e:
            raise RuntimeError(f"MongoDB connection error: {e}")