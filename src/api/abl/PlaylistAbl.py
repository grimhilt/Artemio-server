from flask import jsonify
from ..models import Playlist, PlaylistFile, File, Role
from .. import db
from datetime import datetime
from ..dao.Playlist import PlaylistDao
from flask_login import current_user
from screen.ScreenManager import ScreenManager

class PlaylistAbl:
    @staticmethod
    def create(data):
        roles_edit = db.session.query(Role).filter(Role.id.in_(data['edit'])).all()
        roles_view = db.session.query(Role).filter(Role.id.in_(data['view'])).all()

        new_playlist = Playlist(name=data['name'], owner_id=current_user.as_dict()['id'])
        for role in roles_edit:
            new_playlist.edit.append(role)

        for role in roles_view:
            new_playlist.view.append(role)
        
        db.session.add(new_playlist)
        db.session.flush()
        db.session.commit()

        res = new_playlist.as_dict()
        res['last_modified'] = res['last_modified'].isoformat()
        return jsonify(res)

    @staticmethod
    def update(playlist_id, data): 
        playlist = db.session.query(Playlist).get(playlist_id)

        if 'view' in data:
            roles_view = db.session.query(Role).filter(Role.id.in_(data['view'])).all()
            playlist.view = roles_view

        if 'edit' in data:
            roles_edit = db.session.query(Role).filter(Role.id.in_(data['edit'])).all()
            playlist.edit = roles_edit

        if 'name' in data:
            playlist.name = data['name']

        db.session.flush()
        db.session.commit()
        return jsonify(playlist.as_dict_with_roles())

    @staticmethod
    def get_playlist(playlist_id):
        (query, files) = PlaylistDao.get_playlist(playlist_id)
        query = query.as_dict_with_roles()
        return jsonify({ \
                'id': query['id'], \
                'name': query['name'], \
                'owner_id': query['owner_id'], \
                'view': query['view'], \
                'edit': query['edit'], \
                'files': files})

    @staticmethod
    def list():
        playlists = db.session.query(Playlist).all()
        res = []
        for playlist in playlists:
            p = playlist.as_dict()
            p['last_modified'] = p['last_modified'].isoformat()
            res.append(p)

        return jsonify(res)


    # EDIT PLAYLIST CONTENT
    @staticmethod
    def add_file(playlist_id, data):
        new_playlist_file = PlaylistFile( \
                playlist_id=playlist_id, \
                file_id=data['file_id'], \
                position=data['position'], \
                seconds=data['seconds'] \
                )

        db.session.add(new_playlist_file)
        db.session.commit()
        return jsonify(success=True)

    @staticmethod
    def change_order(playlist_id, data):
        db.session.query(PlaylistFile) \
                .filter(PlaylistFile.file_id == data['file_id']) \
                .filter(PlaylistFile.playlist_id == playlist_id) \
                .update({'position': data['position']})
        db.session.commit()
        return jsonify(success=True)

    @staticmethod
    def change_seconds(playlist_id, data):
        db.session.query(PlaylistFile) \
                .filter(PlaylistFile.file_id == data['file_id']) \
                .filter(PlaylistFile.playlist_id == playlist_id) \
                .update({'seconds': data['seconds']})
        db.session.commit()
        return jsonify(success=True)

    @staticmethod
    def remove_file(playlist_id, data):
        query = db.session.query(PlaylistFile) \
                .filter(PlaylistFile.file_id == data['file_id']) \
                .first()
        db.session.delete(query)
        db.session.commit()
        return jsonify(success=True)
