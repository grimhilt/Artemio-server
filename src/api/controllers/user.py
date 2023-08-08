from flask import Blueprint, request, jsonify
from ..models import User
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import User
from .. import db
from flask_login import login_required, current_user
from ..abl.UserAbl import UserAbl
from ..permissions import Perm, permissions

user = Blueprint('user', __name__)

@user.route('/users', methods=['POST'])
@login_required
@permissions.require([Perm.CREATE_USER])
def create():
    return UserAbl.create(request.get_json())

@user.route('delete', methods=['DELETE'])
def delete():
    return "ok"

@user.route('/users', methods=['GET'])
@login_required
def list():
    return UserAbl.list()
