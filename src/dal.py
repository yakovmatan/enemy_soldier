from pymongo.errors import PyMongoError
from src.db_connection import DbConnection
from src.soldier import Soldier


class Dal:

    def __init__(self):
        self.connection = DbConnection()

    @staticmethod
    def check_soldier(soldier_dict: dict):
        try:
            soldier_obj = Soldier(soldier_dict['soldier_id'],soldier_dict['first_name'],soldier_dict['last_name'],soldier_dict['phone_number'], soldier_dict['rank'])
            return soldier_obj.__dict__
        except Exception as e:
            print(f"Invalid soldier data: {e}")
            return None

    def find_all(self):
        try:
            collection = self.connection.db[self.connection.collection_name]
            return list(collection.find({}, {"_id": 0}))
        except PyMongoError as e:
            print(f"Error reading data: {e}")
            return []

    def insert_soldier(self, soldier: dict):
        try:
            valid_soldier = Dal.check_soldier(soldier)
            if not valid_soldier:
                print("Soldier validation failed. Not inserting.")
                return None

            collection = self.connection.db[self.connection.collection_name]
            return collection.insert_one(valid_soldier).inserted_id
        except PyMongoError as e:
            print(f"Error inserting data: {e}")
            return None
