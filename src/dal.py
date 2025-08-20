from pymongo.errors import PyMongoError
from db_connection import DbConnection
from soldier import Soldier


class Dal:

    def __init__(self):
        self.connection = DbConnection()
        self.collection = self.connection.db[self.connection.collection_name]

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
            return list(self.collection.find({}, {"_id": 0}))
        except PyMongoError:
            return {"error": "database_error"}

    def insert_soldier(self, soldier: dict):
        try:
            if self.collection.find_one({"soldier_id": soldier.get("soldier_id")}):
                return {"error": "soldier_exists"}

            valid_soldier = Dal.check_soldier(soldier)
            if not valid_soldier:
                return {"error": "validation_failed"}

            result = self.collection.insert_one(valid_soldier)
            return {"inserted": "the soldier was successfully inserted.", "inserted_id": str(result.inserted_id)}

        except PyMongoError:
            return {"error": "database_error"}

    def update_soldier(self, soldier_id, field, value):
        try:
            result = self.collection.update_one({"soldier_id": soldier_id},{"$set": {field: value}})
            if result.matched_count == 0:
                return {"error": "soldier_not_found"}

            return {"modified_count": result.modified_count}

        except PyMongoError:
            return {"error": "database_error"}

    def delete_soldier(self, soldier_id):
        try:
            result = self.collection.delete_one(({"soldier_id": soldier_id}))

            if result.deleted_count == 0:
                return {"error": "soldier_not_found"}

            return {"deleted_count": result.deleted_count}

        except PyMongoError:
            return {"error": "database_error"}

