from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user
from ..models import User, Role
from .. import db

def is_current_admin():
    return current_user.as_dict()['roles'][0]['parent_id'] is None


class UserAbl:

    @staticmethod
    def create(data):
        login = data['login']
        password = data['password']
        permissions = data['permissions']

        # check if the user exists
        user = db.session.query(User).filter_by(login=login).first()
        if user:
            return jsonify(user.as_dict()), 302

        # check the user has the permissions he gives to the new user
        user_perms = bin(current_user.as_dict()['roles'][0]['permissions'])
        for (position, bit) in enumerate(bin(permissions)):
            if bit == '1' and bit != user_perms[position]:
                return jsonify(message="You don't have the permission to give permission(s) you don't have"), 403

        # create the user
        new_user = User( \
                login=login, \
                password=generate_password_hash(password, method='sha256') \
                )

        db.session.add(new_user)
        db.session.flush()

        # create the permissions for the user
        new_role = Role( \
                name=login, \
                user_id=new_user.as_dict()['id'], \
                parent_id=current_user.as_dict()['roles'][0]['id'], \
                permissions=permissions)
        db.session.add(new_role)
        new_user.roles.append(new_role)
        db.session.flush()

        db.session.commit()
        return jsonify(new_user.as_dict())

    @staticmethod
    def update(user_id, data):
        return jsonify()

    @staticmethod
    def list():
        query = db.session.query(User).all()
        return jsonify([user.as_dict() for user in query])

    @staticmethod
    def delete(user_id):
        user = db.session.query(User).filter_by(id=user_id).first()
        if not user:
            return jsonify(message="This user doesn't exist or has already been deleted"), 404

        if not is_current_admin and user.as_dict()['roles'][0]['parent_id'] != current_user.as_dict()['roles'][0]['id']:
            # todo all parent should be able to delete
            return jsonify(message="You cannot delete an user you are not the origin of"), 403

        db.session.delete(user)
        # todo check if need to delete the role
        db.session.commit()
        return jsonify(sucess=True)


