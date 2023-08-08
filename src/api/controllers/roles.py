from flask import Blueprint, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
from ..models import Role
from .. import db

roles = Blueprint('roles', __name__)

@roles.route('/roles', methods=['POST'])
@login_required
def create():
    data = request.get_json()
    parent_id = data['parent_id'] if "parent_id" in data else None
    can_create_role = data['can_create_role'] if data['can_create_role'] else False
    can_create_playlist = data['can_create_playlist'] if data['can_create_playlist'] else False
    name = data['name']

    role = db.session.query(Role).filter_by(name=name).first()
    if role:
        return jsonify(message="A role with this name already exists"), 400

    new_role = Role(name=name, parent_id=parent_id, can_create_role=can_create_role, can_create_playlist=can_create_playlist)
    db.session.add(new_role)
    db.session.flush()
    db.session.commit()
    return jsonify(new_role.as_dict())

@roles.route('/roles/<int:role_id>', methods=["GET"])
@login_required
def get(role_id):
    role = db.session.query(Role).filter_by(id=role_id).first()
    if role:
        return jsonify(role.as_dict())
    return jsonify(), 404

@roles.route('/roles', methods=["GET"])
@login_required
def list():
    res = db.session.query(Role).all()
    roles = []
    for role in roles:
        roles.append(role.as_dict())
        
    return jsonify(roles)

