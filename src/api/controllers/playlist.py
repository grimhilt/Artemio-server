from flask import Blueprint, request, Response, jsonify
from flask_cors import cross_origin
from ..models import Playlist, PlaylistFile, File
from .. import db
from datetime import datetime
from sqlalchemy.sql import func
from ..dao.Playlist import PlaylistDao
from flask_login import login_required, current_user
from ..abl.PlaylistAbl import PlaylistAbl
from screen.ScreenManager import ScreenManager
from ..permissions import Perm, permissions

playlist = Blueprint('playlist', __name__)

@playlist.route('', methods=['POST'])
@login_required
@permissions.require([Perm.CREATE_PLAYLIST])
def create():
    return PlaylistAbl.create(request.get_json())

@playlist.route('/playlists', methods=["GET"])
@login_required
def list():
    print(current_user)
    playlists = db.session.query(Playlist).all()

    res = []
    for playlist in playlists:
        p = playlist.as_dict()
        p['last_modified'] = p['last_modified'].isoformat()
        res.append(p)

    return jsonify(res)

@playlist.route('/playlists/<int:playlist_id>', methods=["GET"])
@login_required
@permissions.require([Perm.VIEW_PLAYLIST])
def get_playlist(playlist_id):
    return PlaylistAbl.get_playlist(playlist_id)

# EDIT PLAYLIST

@playlist.route('/playlists/<int:playlist_id>', methods=["POST"])
@login_required
@permissions.require([Perm.EDIT_PLAYLIST])
def add_file(playlist_id):
    return PlaylistAbl.add_file(request.get_json())
    
@playlist.route('/playlists/<int:playlist_id>/order', methods=["POST"])
@login_required
@permissions.require([Perm.EDIT_PLAYLIST])
def change_order(playlist_id):
    return PlaylistAbl.change_order(request.get_json())

@playlist.route('/playlits/<int:playlist_id>/seconds', methods=["POST"])
@login_required
@permissions.require([Perm.EDIT_PLAYLIST])
def change_seconds(playlist_id):
    return PlaylistAbl.change_seconds(request.get_json())

@playlist.route('/playlists/<int:playlist_id>/remove_file', methods=["POST"])
@login_required
@permissions.require([Perm.EDIT_PLAYLIST])
def remove_file(playlist_id):
    return PlaylistAbl.remove_file(request.get_json())

@playlist.route('/playlists/<int:playlist_id>/update', methods=["PUT"])
@login_required
@permissions.require([Perm.OWN_PLAYLIST])
def update(playlist_id):
    return PlaylistAbl.update(playlist_id, request.get_json())

@playlist.route('/playlists/<int:playlist_id>/activate', methods=["POST"])
@login_required
def activate(playlist_id):
    screen_manager = ScreenManager.getInstance() 
    screen_manager.activate_playlist(playlist_id)
    return jsonify(success=True)

@playlist.route('/playlists/<int:playlist_id>/disactivate', methods=["POST"])
@login_required
def disactivate(playlist_id):
    screen_manager = ScreenManager.getInstance() 
    screen_manager.disactivate_playlist()
    return jsonify(success=True)
