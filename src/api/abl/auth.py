from flask import Blueprint, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
from ..models import User

from .. import db
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    login = data['login']
    password = data['password']
    user = db.session.query(User).filter_by(login=login).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify(message="Incorrect credentials"), 401
    login_user(user)
    return jsonify(success=True)


@auth.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    login = data['login']
    password = data['password']
    user = db.session.query(User).filter_by(login=login).first()
    if user:
        return jsonify(user.as_dict_safe()), 302

    new_user = User(login=login, password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.flush()
    db.session.commit()
    return jsonify(new_user.as_dict_safe())

@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify(success=True)

@auth.route('/profile')
@login_required
def profile():
    return jsonify(current_user.as_dict_safe())

