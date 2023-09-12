from .. import db
from ..models import Playlist, PlaylistFile, File

class PlaylistDao:
    def get_playlist(playlist_id):
        query = db.session.query(Playlist).filter(Playlist.id == playlist_id).first()
        files = []
        for playlist_file in query.playlist_files:
            file = playlist_file.file.as_dict()
            file['pfid'] = playlist_file.id
            file['position'] = playlist_file.position
            file['seconds'] = playlist_file.seconds
            files.append(file)

        return (query, files)

    def get_playlist_q(playlist_id):
        query = db.session.query(Playlist).filter(Playlist.id == playlist_id).first()
        return query

    def has_role_view_d(playlist_id, user_id):
        has_role_to_view = db.session.query(Playlist) \
                .filter(Playlist.id == playlist_id) \
                .filter( \
                Playlist.view.any( \
                # check if a role belongs to this user
                Role.user_id == user_id or \
                # check if a this user has a role to view
                Role.users.any(User.id == user_id) \
                )) \
                .first()
        return has_role_to_view

    def has_role_view_d(playlist_id, user_id):
        has_role_to_edit = db.session.query(Playlist) \
                .filter( \
                Playlist.edit.any( \
                # check if a role belongs to this user
                Role.user_id == user_id or \
                # check if a this user has a role to edit
                Role.users.any(User.id == user_id) \
                )) \
                .first()
        return has_role_to_edit
