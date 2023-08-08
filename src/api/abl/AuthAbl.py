from flask import Blueprint, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
from ..models import User, Role, UserRole
from .. import db

class AuthAbl:

    @staticmethod
    def signup(data):
        login = data['login']
        password = data['password']

        is_first_user = db.session.query(User).count() == 0

        if not is_first_user:
            return jsonify(message="You cannot create an account"), 401

        user = db.session.query(User).filter_by(login=login).first()
        if user:
            return jsonify(user.as_dict()), 302

        new_user = User(login=login, password=generate_password_hash(password, method='sha256'))

        if is_first_user:
            new_role = Role(name="admin", can_create_role=True, can_create_playlist=True)
            db.session.add(new_role)
            new_user.roles.append(new_role)

        db.session.add(new_user)
        db.session.flush()
        db.session.commit()
        return jsonify(new_user.as_dict())


    @staticmethod
    def login(data):
        login = data['login']
        password = data['password']

        user = db.session.query(User).filter_by(login=login).first()
        if not user:
            nb_users = db.session.query(User).count()
            if nb_users == 0:
                user = User(login=login, password=generate_password_hash(password, method='sha256'))
                db.session.add(user)
                db.session.flush()
                new_role = Role(name=login, permissions=0b111, user_id=user.as_dict()['id'])
                db.session.add(new_role)
                db.session.flush()
                user.roles.append(new_role)
                db.session.commit()
                login_user(user)
                return jsonify(user.as_dict())
            else:
                return jsonify(message="Incorrect credentials"), 401

        login_user(user)
        return jsonify(user.as_dict())

    @staticmethod
    def profile():
        pr = current_user.as_dict()
        return jsonify(pr)

