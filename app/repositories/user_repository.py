from pymongo import MongoClient
import os

database_url = os.getenv('DATABASE_URL')
 
client = MongoClient(database_url)
db = client.libraryapp
users = db.users

class UserRepository:
    @staticmethod
    def create_user(new_user):
        users.insert_one(new_user)

    @staticmethod
    def find_user_by_email(email):
        return users.find_one({"email": email})

    @staticmethod
    def user_exists(email):
        return bool(users.find_one({"email": email}))
