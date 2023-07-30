from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class PlaylistFile(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'))
#    file_id = db.Column(db.Integer, db.ForeignKey('file.id'))

class File(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150))
    type = db.Column(db.String(255)) # maximum length of mimetype

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150))
    last_modified = db.Column(db.DateTime(timezone=True), default=func.now())
    read_permissions = db.Column(db.Integer, default=0)
    write_permissions = db.Column(db.Integer, default=0)
    execute_permissions = db.Column(db.Integer, default=0)
    files = db.relationship('PlaylistFile')

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(150))
    password = db.Column(db.String(150))
