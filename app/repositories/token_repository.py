from pymongo import MongoClient
import os

database_url = os.getenv('DATABASE_URL')

client = MongoClient(database_url)
db = client.libraryapp
token_blacklist = db.token_blacklist 

class TokenRepository:
    @staticmethod
    def add_token_to_blacklist(token):
        token_blacklist.insert_one({"token": token})
        return True

    @staticmethod
    def is_token_in_blacklist(token):
        return bool(token_blacklist.find_one({"token": token}))
