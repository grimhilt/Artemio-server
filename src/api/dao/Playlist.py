from .. import db
from ..models import Playlist, PlaylistFile, File

class PlaylistDao:
    def get_playlist(playlist_id):
        print(playlist_id)
        print("ok")
        query = db.session.query(Playlist).filter(Playlist.id == playlist_id).first()
        print("ok")
        print(query.files)
        files = []
        for playlist_file in query.files:
            file = playlist_file.file.as_dict()
            file['position'] = playlist_file.position
            file['seconds'] = playlist_file.seconds
            files.append(file)

        return (query, files)
