from pymongo.errors import PyMongoError
from src.db_connection import DbConnection


class Dal:

    def __init__(self):
        self.connection = DbConnection()

