from flask import Blueprint, request, Response, jsonify
from flask_cors import cross_origin
from ..models import Playlist, PlaylistFile
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

    print(new_playlist.as_dict())
    return Response(
            response=new_playlist.as_dict(),
            status=200,
            mimetype="application/json"
        )

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
    query = db.session.query(\
            Playlist.name,\
            func.group_concat(PlaylistFile.id).label('files')\
        ).\
        join(PlaylistFile, Playlist.id == PlaylistFile.playlist_id).\
        filter(Playlist.id == playlist_id).\
        group_by(Playlist.id).\
        all()

    query = db.session.query( \
            Playlist.name, \
            func.group_concat(Playlist.id == PlaylistFile.playlist_id) \
            ) \
        .outerjoin(PlaylistFile, Playlist.id == PlaylistFile.playlist_id) \
        .filter(Playlist.id == playlist_id) \
        .group_by(Playlist.id) \
        .first()

    return jsonify({'name': query[0], 'files': query[1]})

