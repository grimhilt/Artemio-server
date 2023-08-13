from enum import IntEnum
import functools
from flask import request, jsonify
from flask_login import current_user
from . import db
from .models import Playlist, PlaylistFile, User, Role, UserRole

class Perm(IntEnum):
    CREATE_USER = 0
    CREATE_ROLE = 1
    CREATE_PLAYLIST = 2
    VIEW_PLAYLIST = 3
    OWN_PLAYLIST = 4
    EDIT_PLAYLIST = 5
    ACTIVATE_PLAYLIST = 6

class permissions:
    
    @staticmethod
    def require(permissions):
        def decorator_require_permissions(func):
            @functools.wraps(func)
            def wrapper_require_permissions(*args, **kwargs):
                print("wrapper permissions")
                for perm in permissions:
                    check_perm = CheckPermissionFactory(perm)
                    print(args, kwargs)
                    if not check_perm.is_valid(kwargs):
                        return jsonify( \
                                message=check_perm.message), \
                                check_perm.status_code
                return func(*args, **kwargs)

            return wrapper_require_permissions

        return decorator_require_permissions

    
def CheckPermissionFactory(perm):
    print(perm)
    match perm:
        case Perm.CREATE_USER:
            return CheckCreateUser()
        case Perm.CREATE_ROLE:
            return CheckCreateRole()
        case Perm.CREATE_PLAYLIST:
            return CheckCreatePlaylist()
        case Perm.VIEW_PLAYLIST:
            return CheckViewPlaylist()
        case Perm.OWN_PLAYLIST:
            return CheckOwnPlaylist()
        case Perm.EDIT_PLAYLIST:
            return CheckEditPlaylist()
        case Perm.ACTIVATE_PLAYLIST:
            return CheckActivatePlaylist()
        case _:
            return CheckNone()

def get_playlist_id(args):
    if 'playlist_id' in args:
        return args['playlist_id'] 
    json = request.get_json()
    if 'playlist_id' in json:
        print("in")
        return json['playlist_id']
    return

def checkBit(permissions, index):
    binStr = bin(permissions)
    lenStr = len(binStr)
    print(binStr)
    print(lenStr)
    print(lenStr - index)
    return binStr[lenStr - index - 1] == '1'

class CheckNone:
    def is_valid(self, args):
        return True

class CheckOwnPlaylist:
    def __init__(self):
        self.message = "You don't own this playlist"
        self.status_code = 403

    def is_valid(self, args):
        playlist_id = get_playlist_id(args)
        query = db.session.query(Playlist).filter(Playlist.id == playlist_id).first()
        if query is None:
            self.message = "This playlist doesn't exist"
            self.status_code = 404
            return False
        print(query.as_dict())
        return query.as_dict()['owner_id'] == current_user.as_dict()['id']

class CheckViewPlaylist:
    def __init__(self):
        self.message = "You don't have the permission to view this playlist"
        self.status_code = 403

    def is_valid(self, args):
        # if can edit can view, edit check also for owner
        check_edit = CheckEditPlaylist()
        if check_edit.is_valid(args):
            return True
        elif check_edit.status_code == 404:
            self.message = "This playlist doesn't exist"
            self.status_code = 404
            return False

        playlist_id = get_playlist_id(args)
        user_id = current_user.as_dict()['id']
        has_role_to_view = db.session.query(Playlist) \
                .filter( \
                Playlist.view.any( \
                # check if a role belongs to this user
                Role.user_id == user_id or \
                # check if a this user has a role to view
                Role.users.any(User.id == user_id) \
                )) \
                .first()
        return has_role_to_view is not None

class CheckEditPlaylist:
    def __init__(self):
        self.message = "You don't have the permission to edit this playlist"
        self.status_code = 403

    def is_valid(self, args):
        check_own = CheckOwnPlaylist()
        if check_own.is_valid(args):
            return True
        elif check_own.status_code == 404:
            self.message = "This playlist doesn't exist"
            self.status_code = 404
            return False

        playlist_id = get_playlist_id(args)
        user_id = current_user.as_dict()['id']
        has_role_to_edit = db.session.query(Playlist) \
                .filter( \
                Playlist.edit.any( \
                # check if a role belongs to this user
                Role.user_id == user_id or \
                # check if a this user has a role to edit
                Role.users.any(User.id == user_id) \
                )) \
                .first()
        return has_role_to_edit is not None

class CheckCreateUser:
    def __init__(self):
        self.message = "You don't have the permission to create an user"
        self.status_code = 403

    def is_valid(self, _):
        return checkBit(current_user.as_dict()['roles'][0]['permissions'], Perm.CREATE_USER)

class CheckCreatePlaylist:
    def __init__(self):
        self.message = "You don't have the permission to create a playlist"
        self.status_code = 403

    def is_valid(self, _):
        return checkBit(current_user.as_dict()['roles'][0]['permissions'], Perm.CREATE_PLAYLIST)

class CheckActivatePlaylist:
    def __init__(self):
        self.message = "You don't have the permission to activate this playlist"
        self.status_code = 403

    def is_valid(self, args):
        check_own = CheckOwnPlaylist()
        if check_own.is_valid(args):
            return True
        elif check_own.status_code == 404:
            self.message = "This playlist doesn't exist"
            self.status_code = 404
            return False

        # todo check view
        return False

