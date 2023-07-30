from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import path
import logging


db = SQLAlchemy()
DB_NAME = 'database.db'


def create_api():
    app = Flask(__name__)
    CORS(app)
    logging.getLogger('flask_cors').level = logging.DEBUG
    #CORS(app, resources={r"/*": {"origin": ["http://localhost:3008"]}})
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .abl.user import user
    from .abl.playlist import playlist
    from .abl.file import file

    app.register_blueprint(user, url_prefix='/api/user')
    app.register_blueprint(playlist, url_prefix='/api/playlist')
    app.register_blueprint(file, url_prefix='/api/file')

    from .models import User, Playlist, PlaylistFile, File

    with app.app_context():
        db.create_all()


    return app
