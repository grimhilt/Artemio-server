from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager
from os import path
import logging


db = SQLAlchemy()
DB_NAME = 'database.db'


def create_api():
    app = Flask(__name__)
    CORS(app)
    logging.getLogger('flask_cors').level = logging.DEBUG
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.secret_key = b'_5#y2L"F4Qfj8zxec]'

    login_manager = LoginManager()
    login_manager.init_app(app)

    db.init_app(app)

    from .controllers.user import user
    from .controllers.playlist import playlist
    from .controllers.file import file
    from .controllers.auth import auth
    from .controllers.roles import roles

    app.register_blueprint(user, url_prefix='/api')
    app.register_blueprint(playlist, url_prefix='/api')
    app.register_blueprint(file, url_prefix='/api/file')
    app.register_blueprint(auth, url_prefix='/api/auth')
    app.register_blueprint(roles, url_prefix='/api')

    from .models import User, Playlist, PlaylistFile, File
    
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(int(user_id))

    with app.app_context():
        db.create_all()


    return app
