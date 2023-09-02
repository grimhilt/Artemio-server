# Artemio (server)

# Deployment (from source)

- ``git clone https://github.com/grimhilt/artemio-server.git``

python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

# Documentation
## API

/api/login
/api/logout

### Playlists (*/api/playlists*)

The user need to be logged in for every routes

| Method | Endpoint | Permission | Description
| --- | --- | --- | --- |
| POST | ``/api/playlists`` | CREATE_PLAYLIST |
| GET  | ``/api/playlists`` |  |
| GET  | ``/api/playlists/:id`` | VIEW_PLAYLIST |
| POST | ``/api/playlists/:id`` | EDIT_PLAYLIST | Add file to playlist
| POST | ``/api/playlists/:id/order`` | EDIT_PLAYLIST | Change file order
| POST | ``/api/playlists/:id/seconds`` | EDIT_PLAYLIST | Change display time of a file
| POST | ``/api/playlists/:id/remove_file`` | EDIT_PLAYLIST |
| PUT  | ``/api/playlists/:id/update`` | OWN_PLAYLIST |
| POST | ``/api/playlists/:id/activate`` | ACTIVATE_PLAYLIST |
| POST | ``/api/playlists/:id/disactivate`` | ACTIVATE_PLAYLIST |

### Users

### Roles

### 