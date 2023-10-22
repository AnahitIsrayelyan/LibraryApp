import io
from bson import ObjectId, Binary
from flask import send_file, jsonify
from werkzeug.utils import secure_filename
from app.repositories.book_repository import BookRepository
from app.repositories.token_repository import TokenRepository
from app.services.token_service import validate_token

def get_books(): 
    # Query the database for all books
    books_info = BookRepository.find_books({})
    # Convert the result to a list of dictionaries and Convert the _id field to a string for each book
    books_list = [{"_id": str(book["_id"]), "name": book["name"], "author_name": book["author_name"], "tag": book["tag"]} for book in books_info]
    
    return jsonify({"books": books_list}), 200


def filter_books(filter_dict):
    # print(filter_dict, "service")
    # Query the database for books that match the filter criteria
    books_cursor = BookRepository.find_books(filter_dict)
    # Convert the result to a list of dictionaries and Convert the _id field to a string for each book
    books_list = [{"_id": str(book["_id"]), "name": book["name"], "author_name": book["author_name"], "tag": book["tag"]} for book in books_cursor]
    
    return jsonify({"books": books_list}), 200


def get_book_info(book_id):
    try:
        # Query the database for the book with the specified ID
        book = BookRepository.find_book_by_id(book_id)
        # Create a dictionary with only the required fields
        book_info = {
            "id": str(book["_id"]),
            "name": book["name"],
            "author_name": book["author_name"],
            "tag": book["tag"]
        }
        # Return the book info as JSON
        return {"book": book_info}, 200
    except Exception as e:
        return {"message": "Error fetching book info", "error": str(e)}, 500


def download_book(book_id):
    try:
        # Query the database for the book with the specified ID
        book = BookRepository.find_book_by_id(book_id)
        # If the book is not found, return a 404 error
        if book is None:
            return jsonify({"message": "Book not found"}), 404
        # Get the binary data of the file
        binary_data = book['file']['data']
        # Convert the binary data to a byte stream
        byte_stream = io.BytesIO(binary_data)
        # Set the content type and the original filename
        content_type = book['file']['contentType']
        original_name = book['file']['originalName']
        # Return the byte stream as a file download
        return send_file(byte_stream, mimetype=content_type, as_attachment=True, download_name=original_name)
    except Exception as e:
        return {"message": "Error downloading book", "error": str(e)}, 500


def upload_book(form, files):
    # Get the name and tag fields from the form data
    name = form.get('name')
    tag = form.get('tag')
    author_name = form.get('author_name')

    # Check if a file was uploaded
    if 'file' not in files:
        return jsonify({"message": "No file uploaded"}), 400

    # Get the uploaded file
    file = files['file']
    filename = secure_filename(file.filename)

    # Convert the file to a Binary object
    binary_data = Binary(file.read())

    new_book = {
        "name": name,
        "author_name": author_name,
        "tag": tag,
        "file": {
            "filename": filename,
            "originalName": filename,
            "contentType": file.content_type,
            "data": binary_data
        }
    }

    BookRepository.create_book(new_book)

    return jsonify({"message": "Book uploaded successfully"}), 201

def update_book(book_id, form, files):
    # Create a dictionary of fields to update
    update_fields = {}
    if 'name' in form:
        update_fields['name'] = form.get('name')
    if 'tag' in form:
        update_fields['tag'] = form.get('tag')
    if 'author_name' in form:
        update_fields['author_name'] = form.get('author_name')

    # Check if a file was uploaded
    if 'file' in files:
        file = files['file']
        filename = secure_filename(file.filename)

        # Convert the file to a Binary object
        binary_data = Binary(file.read())

        # Update the file details in the update_fields dictionary
        update_fields['file.filename'] = filename
        update_fields['file.originalName'] = filename
        update_fields['file.contentType'] = file.content_type
        update_fields['file.data'] = binary_data

    # Update the book details in the database
    BookRepository.update_book(book_id, update_fields)

    return jsonify({"message": "Book updated successfully"}), 200

def delete_book(book_id):
    # Delete the book from the database
    BookRepository.delete_book(book_id)

    return jsonify({"message": "Book deleted successfully"}), 200
