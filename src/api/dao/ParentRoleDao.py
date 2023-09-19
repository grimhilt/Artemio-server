from .. import db
from ..models import User, Role, Playlist, ParentRole

class ParentRoleDao:
    def get_children(role_id):
        children = db.session.query(ParentRole) \
                .filter(ParentRole.parent_id == role_id) \
                .all()
        return children

    def get_parents(role_id):
        parents = db.session.query(ParentRole) \
                .filter(ParentRole.child_id == role_id) \
                .all()
        return parents
