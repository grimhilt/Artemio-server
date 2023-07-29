from flask import Blueprint, request
from ..models import User
from werkzeug.security import generate_password_hash, check_password_hash

user = Blueprint('user', __name__)

@user.route('create', methods=['PUT'])
def create():
    print(request.get_json()) 
    return "ok"
    generate_password_hash("i", method='sha256')
    db.session.add(new_user)
    db.session.commit()
    return "ok"

@user.route('delete', methods=['DELETE'])
def delete():
    return "ok"

@user.route('list', methods=['GET'])
def list():
    return "ok"
