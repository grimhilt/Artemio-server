from flask import Blueprint, request, Response, jsonify
from flask_cors import cross_origin
from ..models import Playlist, PlaylistFile, File
from .. import db
from datetime import datetime
from sqlalchemy.sql import func

playlist = Blueprint('playlist', __name__)

@playlist.route('/', methods=['PUT'])
def create():
    data = request.get_json()
    new_playlist = Playlist(name=data['name'])
    db.session.add(new_playlist)
    db.session.flush()
    db.session.commit()

    res = new_playlist.as_dict()
    res['last_modified'] = res['last_modified'].isoformat()
    return jsonify(res)

@playlist.route('/', methods=["GET"])
def list():
    playlists = db.session.query(Playlist).all()

    res = []
    for playlist in playlists:
        p = playlist.as_dict()
        p['last_modified'] = p['last_modified'].isoformat()
        res.append(p)

    return jsonify(res)

@playlist.route('/<int:playlist_id>', methods=["GET"])
def get_playlist(playlist_id):
    query = db.session.query(Playlist).filter(Playlist.id == playlist_id).first()

    files = []
    for playlist_file in query.playlist_files:
        file = playlist_file.file.as_dict()
        file['position'] = playlist_file.position
        file['seconds'] = playlist_file.seconds
        files.append(file)

    return jsonify({'name': query.name, 'files': files})

@playlist.route('/<int:playlist_id>', methods=["POST"])
def add_file(playlist_id):
    data = request.get_json()
    print(data)
    new_playlist_file = PlaylistFile( \
            playlist_id=playlist_id, \
            file_id=data['file_id'], \
            position=data['position'], \
            seconds=data['seconds'] \
            )

    db.session.add(new_playlist_file)
    db.session.flush()
    db.session.commit()

    return jsonify(success=True)
    
@playlist.route('/<int:playlist_id>/order', methods=["POST"])
def change_order(playlist_id):
    data = request.get_json()
    print(data)
    db.session.query(PlaylistFile) \
            .filter(PlaylistFile.file_id == data['file_id']) \
            .filter(PlaylistFile.playlist_id == playlist_id) \
            .update({'position': data['position']})
    db.session.commit()

    return jsonify(success=True)
