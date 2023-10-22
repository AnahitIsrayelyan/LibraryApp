from pymongo import MongoClient
from bson import ObjectId, Binary
from werkzeug.utils import secure_filename
import os

database_url = os.getenv('DATABASE_URL')


# client = MongoClient("mongodb+srv://anahit:aaaa1111@cluster0.lyujuxw.mongodb.net")
client = MongoClient(database_url)
db = client.libraryapp
books = db.books

class BookRepository:
    @staticmethod
    def create_book(new_book):
        # filename = secure_filename(file.filename)
        # binary_data = Binary(file.read())

        # new_book = {
        #     "name": name,
        #     "author_name": author_name,
        #     "tag": tag,
        #     "file": {
        #         "filename": filename,
        #         "originalName": filename,
        #         "contentType": file.content_type,
        #         "data": binary_data
        #     }
        # }
        books.insert_one(new_book)

    @staticmethod
    def update_book(book_id, update_fields):
        books.update_one(
        {"_id": ObjectId(book_id)},
        {
            "$set": update_fields
        }
    )
         
    @staticmethod
    def find_books(filter_dict):
        # print(filter_dict, "repo")
        return books.find(filter_dict, {"_id": 1, "name": 1, "author_name": 1, "tag": 1})

    @staticmethod
    def find_book_by_id(book_id):
        return books.find_one({"_id": ObjectId(book_id)})
    
    @staticmethod
    def delete_book(book_id):
        books.delete_one({"_id": ObjectId(book_id)})
        return True
