from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class PlaylistFile(db.Model):
    __tablename__ = 'PlaylistFile'
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'), primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('file.id'), primary_key=True)
    position = db.Column(db.Integer)
    seconds = db.Column(db.Integer, default=10)

class File(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(150))
    type = db.Column(db.String(255)) # maximum length of mimetype
    playlists = db.relationship('Playlist', secondary='PlaylistFile', back_populates='files')

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(150))
    owned_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    last_modified = db.Column(db.DateTime(timezone=True), default=func.now())
    read_permissions = db.Column(db.Integer, default=0)
    write_permissions = db.Column(db.Integer, default=0)
    execute_permissions = db.Column(db.Integer, default=0)
    files = db.relationship('File', secondary='PlaylistFile', back_populates='playlists')

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class UserRole(db.Model):
    __tablename__ = 'UserRole'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=True)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    parent_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    can_create_role = db.Column(db.Boolean, default=False)
    can_create_playlist = db.Column(db.Boolean, default=False)
    users = db.relationship('User', secondary='UserRole', back_populates='roles')

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    login = db.Column(db.String(150))
    password = db.Column(db.String(150))
    roles = db.relationship('Role', secondary='UserRole', back_populates='users')

    def as_dict(self):
        res = self.as_dict_unsafe()
        res['roles'] = [role.as_dict() for role in self.roles]
        del res['password']
        return res

    def as_dict_unsafe(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

