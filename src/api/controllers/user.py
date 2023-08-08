from flask import Blueprint, request
from flask_login import login_required
from ..abl.UserAbl import UserAbl
from ..permissions import Perm, permissions

user = Blueprint('user', __name__)

@user.route('/users', methods=['POST'])
@login_required
@permissions.require([Perm.CREATE_USER])
def create():
    return UserAbl.create(request.get_json())

@user.route('/users/<int:user_id>', methods=['DELETE'])
@login_required
@permissions.require([Perm.CREATE_USER])
def delete(user_id):
    return UserAbl.delete(user_id) 

@user.route('/users', methods=['GET'])
@login_required
def list():
    return UserAbl.list()

@user.route('/users/<int:user_id>', methods=['PUT'])
@login_required
@permissions.require([Perm.CREATE_USER])
def update(user_id):
    return UserAbl.update(user_id, request.get_json())
