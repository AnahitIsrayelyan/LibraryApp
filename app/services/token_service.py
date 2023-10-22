import jwt
from app.repositories.token_repository import token_blacklist
from app.repositories.user_repository import users
from app import app


def validate_token(token):
    # Check if the token is in the blacklist
    if token_blacklist.find_one({"token": token}):
        raise jwt.exceptions.DecodeError("You are logged out.")

    payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])

    user_email = payload.get('user_email')

    user = users.find_one({"email": user_email})

    if not user:
        raise jwt.exceptions.DecodeError("User not found")

    return user
