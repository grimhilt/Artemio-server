from flask import Blueprint, request, jsonify, send_file
from ..models import File
from .. import db

files = Blueprint('files', __name__)
FILE_DIR = './data/'

@files.route('/files', methods=['POST'])
def upload():
    res = []
    for file_key in request.files:
        file = request.files[file_key]
        exists = db.session.query(File).filter(File.name == file.filename).first()
        if not exists:
            file.save(FILE_DIR + file.filename)
            new_file = File(name=file.filename, type=file.mimetype)
            db.session.add(new_file)
            db.session.flush()
            res.append(new_file.as_dict().copy())

        db.session.commit()
        return jsonify(res)

@files.route('/files', methods=['GET'])
def list():
    files = db.session.query(File).all()
    res = []
    for file in files:
        res.append(file.as_dict())
    return jsonify(res)

@files.route('/files/<int:file_id>', methods=['GET'])
def load(file_id):
    file = db.session.query(File).filter(File.id == file_id).first()
    return send_file(('../../data/' + file.name), mimetype=file.type)

@files.route('/files/<int:file_id>', methods=['DELETE'])
def delete(file_id):
    rows = db.session.query(File).filter(File.id == file_id).all()
    for row in rows:
        db.session.delete(row)
    db.session.commit()
    return jsonify(success=True)
