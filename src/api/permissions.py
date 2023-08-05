from enum import Enum
import functools
from flask import request, jsonify
from flask_login import current_user
from . import db
from .models import Playlist, PlaylistFile, User, Role, UserRole

Perm = Enum('Perm', ['CREATE_ROLE', 'CREATE_PLAYLIST'])

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
        case _:
            return CheckNone()


class CheckNone:
    def is_valid(self):
        return True

class CheckCreatePlaylist:
    def is_valid(self):
        q = db.session.query(User) \
                .filter_by(id=current_user.as_dict()['id']) \
                .first()
        print(q.as_dict())


