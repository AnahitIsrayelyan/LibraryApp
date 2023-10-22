from flask import Flask
import secrets
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv


app = Flask(__name__)
# my_key = secrets.token_hex(24)
# app.config['SECRET_KEY'] = my_key
load_dotenv()
bcrypt = Bcrypt(app)

from app.views import book_views, user_views