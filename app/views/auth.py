from functools import wraps
from flask import request, jsonify
import jwt
from app import app
from app.repositories.user_repository import users
from app.repositories.token_repository import token_blacklist


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            # Check if the token is in the blacklist
            if token_blacklist.find_one({"token": token}):
                return jsonify({"message": "You are logged out."}), 401

            # Decode the token and get the user email
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            user_email = payload.get('user_email')

            # Query the database for the user with the specified email
            user = users.find_one({"email": user_email})

            # If the user is not found, return a 404 error
            if user is None:
                return jsonify({"message": "User not found"}), 404

            # Add the user to the request object
            request.user = user

            return f(*args, **kwargs)

        except jwt.ExpiredSignatureError:
            # Handle expired token
            return jsonify({"message": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            # Handle invalid token
            return jsonify({"message": "Invalid token"}), 401

    return decorated_function
