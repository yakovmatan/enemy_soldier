from pymongo.errors import PyMongoError
from src.db_connection import DbConnection


class Dal:

    def __init__(self):
        self.connection = DbConnection()

    def find_all(self):
        try:
            collection = self.connection.db[self.connection.collection_name]
            return list(collection.find({}, {"_id": 0}))
        except PyMongoError as e:
            print(f"Error reading data: {e}")
            return []