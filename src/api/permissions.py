from enum import Enum
import functools
from flask import request, jsonify
from flask_login import current_user
from . import db
from .models import Playlist, PlaylistFile, User, Role, UserRole

Perm = Enum('Perm', ['CREATE_ROLE', 'CREATE_PLAYLIST', 'VIEW_PLAYLIST', 'OWN_PLAYLIST', 'EDIT_PLAYLIST'])

class permissions:
    
    @staticmethod
    def require(permissions):
        def decorator_require_permissions(func):
            @functools.wraps(func)
            def wrapper_require_permissions(*args, **kwargs):
                for perm in permissions:
                    check_perm = CheckPermissionFactory(perm)
                    if not check_perm.is_valid():
                        return jsonify( \
                                message=check_perm.message), \
                                check_perm.status_code
                return func(*args, **kwargs)

            return wrapper_require_permissions

        return decorator_require_permissions

    
def CheckPermissionFactory(perm):
    print(perm)
    match perm:
        case Perm.CREATE_ROLE:
            return CheckCreateRole()
        case Perm.CREATE_PLAYLIST:
            print("creat plays")
            return CheckCreatePlaylist()
        case Perm.VIEW_PLAYLIST:
            return CheckViewPlaylist()
        case Perm.OWN_PLAYLIST:
            return CheckOwnPlaylist()
        case Perm.EDIT_PLAYLIST:
            return CheckEditPlaylist()
        case _:
            return CheckNone()


class CheckNone:
    def is_valid(self):
        return True

class CheckOwnPlaylist:
    def is_valid(self, playlist_id):
        query = db.session.query(Playlist).filter(Playlist.id == playlist_id).first()
        self.message = "You don't own this playlist"
        self.status_code = 403
        return query['owner_id'] == current_user.as_dict()['id']

class CheckViewPlaylist:
    def is_valid(self, playlist_id):
        if CheckOwnPlaylist().is_valid(playlist_id):
            return True
        self.message = "You don't have the permission to view this playlist"
        self.status_code = 403
        return False

class CheckEditPlaylist:
    def is_valid(self, playlist_id):
        if CheckOwnPlaylist().is_valid(playlist_id):
            return True

        self.message = "You don't have the permission to edit this playlist"
        self.status_code = 403
        return False

class CheckCreatePlaylist:
    def is_valid(self, _):
        has_role_to_create = next( \
                (True \
                for role in current_user.as_dict()['roles'] \
                if role['can_create_playlist']), \
                None)

        self.message = "You don't have the permission to create a playlist"
        self.status_code = 403
        return has_role_to_create


