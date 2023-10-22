from bson.objectid import ObjectId
from flask import jsonify
import jwt
from app import app, bcrypt
from app.repositories.user_repository import UserRepository
from app.repositories.token_repository import TokenRepository
from jsonschema import validate, ValidationError
from app.repositories.user_repository import UserRepository


def register(data, schema):
    # Validate the request data against the schema
    try:
        validate(data, schema)
    except ValidationError as e:
        return jsonify({"message": "Invalid data", "error": str(e)}), 400

    # Check if the user with that email already exists
    existing_user = UserRepository.find_user_by_email(data['email'])
    if existing_user:
        return jsonify({"message": "This email is already used"}), 409

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    print(hashed_password, type(hashed_password))

    # Add new user
    new_user = {
        "name": data['name'],
        "email": data['email'],
        "password": hashed_password,
        "role": "NEW"
    }

    UserRepository.create_user(new_user)

    return jsonify({"message": "Successfully added"}), 201


def login(data):
    if not data or not data['email'] or not data['password']:
        return jsonify({"message": "Missing data"}), 400

    # Check if user exists
    user = UserRepository.find_user_by_email(data['email'])
    if user and bcrypt.check_password_hash(user["password"], data["password"]):
        token = jwt.encode({"user_email": user['email']}, app.config['SECRET_KEY'], algorithm="HS256")

        user_data = {k: v for k, v in user.items() if k not in ['password', '_id']}

        user_data['token'] = token

        return jsonify(user_data), 200
    
    return jsonify({"message": "Invalid credentials"}), 401


def logout(token):
    # Add the token to the blacklist
    if not token:
        return jsonify({"message": "Token is missing!"}), 401

    TokenRepository.add_token_to_blacklist(token)
    return jsonify({"message": "Logout successful"}), 200

def validate_token(token):
    # Check if the token is in the blacklist
    if TokenRepository.is_token_in_blacklist(token):
        raise jwt.exceptions.DecodeError("You are logged out.")

    payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
    user_email = payload.get('user_email')
    user = UserRepository.find_user_by_email(user_email)

    if not user:
        raise jwt.exceptions.DecodeError("User not found")

    return user
