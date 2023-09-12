from .. import db
from ..models import User, Role, Playlist

class UsersDao:
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


