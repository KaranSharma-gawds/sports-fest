import datetime as datetime
from flask import request, redirect, render_template
from models import UploadedFile, Event
from connection import DatabaseHandler
from . import upload_route
from .upload_file import upload_file

session = DatabaseHandler.connect_to_database()

@upload_route.route('/image/add', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'photo' not in request.files:
            # flash('no photo part in request')
            print('no photo part in request')
            return redirect(request.url)
        photo = request.files['photo']
        obj = upload_file(photo, 'IMG')
        if obj['status'] == 'BAD REQUEST':
            print(obj['message'])
            return obj
        if obj['status'] == 'OK':
            print(obj['message'])
            filename = obj['filename']
            info = UploadedFile(filename=filename, event_id=request.data['event_id'])
            session.add(info)
            session.commit()
            return {
                'status':'OK',
                'message':'SUCCESSFULLY ADDED IMAGE'
            }, 200
        return {
            'status':'ERROR',
            'message':'UNPREDICTED ERROR OCCURRED'
        }
    else:
        return render_template('upload-file.html', filetype='photo', url=request.url)

@upload_route.route('/doc/add', methods=['GET', 'POST'])
def upload_doc():
    if request.method == 'POST':
        if 'doc' not in request.files:
            # flash('no doc part in request')
            print('no doc part in request')
            return redirect(request.url)
        photo = request.files['doc']
        obj = upload_file(photo, 'DOC')
        if obj['status'] == 'BAD REQUEST':
            print(obj['message'])
            return obj
        if obj['status'] == 'OK':
            print(obj['message'])
            filename = obj['filename']
            info = UploadedFile(filename=filename, event_id=request.data['event_id'])
            session.add(info)
            session.commit()
            return {
                'status':'OK',
                'message':'SUCCESSFULLY ADDED DOC'
            }, 200
        return {
            'status':'ERROR',
            'message':'UNPREDICTED ERROR OCCURRED'
        }
    else:
        return render_template('upload-file.html', filetype='doc', url=request.url)

@upload_route.route('/image/get', methods=['GET'])
def load_images():
    event_id = request.data['event_id']
    if not Event.query.filter_by(id=event_id).first():
        return {
            'status':'BAD REQUEST',
            'message':'EVENT DOES NOT EXIST'
        }
    image_records = UploadedFile.query.filter_by(event_id=event_id).all()
    image_url_array = []
    for image_record in image_records:
        image_url_array.append(image_record.filename)
    return {
        'status':'OK',
        'message':'SUCCESS',
        'array':image_url_array
    }, 200

@upload_route.route('/doc/get', methods=['GET'])
def load_docs():
    event_id = request.data['event_id']
    if not Event.query.filter_by(id=event_id).first():
        return {
            'status':'BAD REQUEST',
            'message':'EVENT DOES NOT EXIST'
        }
    doc_records = UploadedFile.query.filter_by(event_id=event_id).all()
    doc_url_array = []
    for doc_record in doc_records:
        doc_url_array.append(doc_record.filename)
    return {
        'status':'OK',
        'message':'SUCCESS',
        'array':doc_url_array
    }, 200
