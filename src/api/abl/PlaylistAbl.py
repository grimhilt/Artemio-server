from flask import jsonify

class PlaylistAbl:
    @staticmethod
    def create(data):
        print("create in")
        return jsonify(), 200
        #new_playlist = Playlist(name=data['name'])
        #db.session.add(new_playlist)
        #db.session.flush()
        #db.session.commit()

        #res = new_playlist.as_dict()
        #res['last_modified'] = res['last_modified'].isoformat()
        #return jsonify(res)
