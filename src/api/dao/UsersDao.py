from .. import db
from ..models import User, Role

class UsersDao:
    def has_role_view_q(user_id):
        has_role_to_view = db.session.query(User) \
                .filter(User.id == user_id) \
                .filter( \
                User.roles.any( \
                    Role.users.any(Role.playlists_view  is not None) \
                )) \
                .first()
        return has_role_to_view

    def has_role_edit_q(user_id):
        has_role_to_edit = db.session.query(User) \
                .filter(User.id == user_id) \
                .filter( \
                User.roles.any( \
                    Role.users.any(Role.playlists_edit  is not None) \
                )) \
                .first()
        return has_role_to_edit

