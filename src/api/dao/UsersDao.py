from .. import db
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import User, Role, Playlist
from .RolesDao import RolesDao

class UsersDao:

    def create(login, password, permissions, current_user):
        # create the user
        new_user = User(
                login=login,
                password=generate_password_hash(password, method='sha256')
                )

        db.session.add(new_user)
        db.session.flush()

        # create role for the user
        new_role = RolesDao.create(
                name=login,
                user_id=new_user.as_dict()['id'],
                parent_id=current_user.as_dict()['roles'][0]['id'],
                permissions=permissions)

        new_user.roles.append(new_role)
        db.session.flush()
        return new_user


    def has_role_view_q(user_id):
        has_role_to_view = db.session.query(User) \
                .filter(User.id == user_id) \
                .filter(
                User.roles.any(
                    Role.users.any(Role.playlists_view  is not None)
                )) \
                .first()
        return has_role_to_view

    def has_role_edit_q(user_id):
        has_role_to_edit = db.session.query(User) \
                .filter(User.id == user_id) \
                .filter(
                User.roles.any(
                    Role.users.any(Role.playlists_edit  is not None)
                )) \
                .first()
        return has_role_to_edit

    def playlists(user_id):
        # todo recursion on user parenting
        playlists = db.session.query(Playlist) \
                .filter(
                # all playlist where user can view
                Playlist.view.any(
                # check if a role belongs to this user
                Role.user_id == user_id or
                # check if a this user has a role to view
                Role.users.any(User.id == user_id) \
                ) |
                # all playlist where user can edit
                Playlist.edit.any(
                    # check if a role belongs to this user
                    Role.user_id == user_id or
                    # check if a this user has a role to edit
                    Role.users.any(User.id == user_id)

                ) |
                (Playlist.owner_id == user_id)
                ) \
                .all()
        return playlists


