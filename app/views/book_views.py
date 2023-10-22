from flask import request, jsonify
from app.services import book_service
from app.models.book import book_schema
from app.views.auth import login_required
from app import app
from app.services.token_service import validate_token


@app.route('/books', methods=['GET'])
@login_required
def get_books():
    return book_service.get_books()

"""
http://127.0.0.1:5000/books/filter?tag=C%2B%2B
http://localhost:5000/books/filter?tag=Python
http://localhost:5000/books/filter?author=Author&tag=Python
"""
@app.route('/books/filter', methods=['GET'])
@login_required 
def filter_books():
    author_name = request.args.get('author')
    tag = request.args.get('tag')
    filter_dict = {}
    if author_name:
        filter_dict['author_name'] = author_name
    if tag:
        filter_dict['tag'] = tag
    # print(filter_dict, "view")
    return book_service.filter_books(filter_dict)


@app.route('/books/<book_id>', methods=['GET'])
@login_required
def get_book_info(book_id):
    return book_service.get_book_info(book_id)


@app.route('/books/download/<book_id>', methods=['GET'])
@login_required
def download_book(book_id):
    token = request.headers.get('Authorization')
    user = validate_token(token)
    if user['role'] == 'BANNED':
        return jsonify({"message": "You are banned and cannot download books"}), 403
    return book_service.download_book(book_id)


@app.route('/books', methods=['POST'])
@login_required
def upload_book():
    token = request.headers.get('Authorization')
    user = validate_token(token)
    if user['role'] != 'ADMIN':
        return jsonify({"message": "Only admin users can upload books"}), 403
    return book_service.upload_book(request.form, request.files)


@app.route('/books/<book_id>', methods=['PUT'])
@login_required
def update_book(book_id):
    token = request.headers.get('Authorization')
    user = validate_token(token)
    if user['role'] != 'ADMIN':
        return jsonify({"message": "Only admin users can update books"}), 403
    return book_service.update_book(book_id, request.form, request.files)


@app.route('/books/<book_id>', methods=['DELETE'])
@login_required
def delete_book(book_id):
    token = request.headers.get('Authorization')
    user = validate_token(token)
    if user['role'] != 'ADMIN':
        return jsonify({"message": "Only admin users can delete books"}), 403
    return book_service.delete_book(book_id)
