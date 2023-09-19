from .. import db
from ..models import User, Role, Playlist, ParentRole
from .ParentRoleDao import ParentRoleDao

class RolesDao:

    def create(name, user_id, parent_id, permissions):
        new_role = Role(
                name=name,
                user_id=user_id,
                parent_id=parent_id,
                permissions=permissions)
        db.session.add(new_role)

        # get all parents
        parents = ParentRoleDao.get_parents(parent_id)         
        parent_ids = [parent_id]
        for parent in parents:
            parent_ids.append(parent.as_dict()['parent_id'])

        # add all parents
        for id in parent_ids:
            parent_role = ParentRole(
                    parent_id=id,
                    child_id=user_id
                    )
            db.session.add(parent_role)

        db.session.flush()
        return new_role

