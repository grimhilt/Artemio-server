from flask import Blueprint, request, jsonify
from flask_login import login_required, logout_user
from ..abl.AuthAbl import AuthAbl

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    return AuthAbl.login(request.get_json()) 

@auth.route('/signup', methods=['POST'])
def signup():
    return AuthAbl.signup(request.get_json())

@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify(success=True)

@auth.route('/profile')
@login_required
def profile():
    return AuthAbl.profile()
