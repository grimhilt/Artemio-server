from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class PlaylistFile(db.Model):
    __tablename__ = 'PlaylistFile'
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'), primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('file.id'), primary_key=True)
    position = db.Column(db.Integer)
    seconds = db.Column(db.Integer, default=10)
    playlist = db.relationship('Playlist', back_populates='playlist_files')
    file = db.relationship('File', back_populates='playlist_files')

class File(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(150))
    type = db.Column(db.String(255)) # maximum length of mimetype
    playlist_files = db.relationship('PlaylistFile', back_populates='file')

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(150))
    last_modified = db.Column(db.DateTime(timezone=True), default=func.now())
    read_permissions = db.Column(db.Integer, default=0)
    write_permissions = db.Column(db.Integer, default=0)
    execute_permissions = db.Column(db.Integer, default=0)
    files = db.relationship('File', secondary='PlaylistFile')
    playlist_files = db.relationship('PlaylistFile', order_by='PlaylistFile.position', back_populates='playlist')

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    login = db.Column(db.String(150))
    password = db.Column(db.String(150))
