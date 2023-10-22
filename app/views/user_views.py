from flask import request
from app.services import user_service
from app.models.user import user_schema
from app import app
from app.views.auth import login_required


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    return user_service.register(data, user_schema)

 
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return user_service.login(data)


@app.route('/logout', methods=['POST'])
@login_required
def logout(): 
    token = request.headers.get('Authorization')
    return user_service.logout(token)
