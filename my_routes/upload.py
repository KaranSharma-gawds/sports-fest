import datetime as datetime
from flask import request, redirect, render_template
from models import UploadedFile, Event
from connection import DatabaseHandler
from flask_login import login_required
from . import upload_route
from .upload_file import upload_file

session = DatabaseHandler.connect_to_database()
@upload_route.route('/image/add', methods=['POST'])
@login_required
def upload_image():
    if 'photo' not in request.files:
        # flash('no photo part in request')
        print('no photo part in request')
        session.close()
        return redirect(request.url)
    photo = request.files['photo']
    obj = upload_file(photo, 'IMG')
    if obj['status'] == 'BAD REQUEST':
        print(obj['message'])
        return obj
    if obj['status'] == 'OK':
        print(obj['message'])
        filename = obj['filename']
        info = UploadedFile(filename=filename, file_type='IMAGE')
        session.add(info)
        session.commit()
        session.close()
        return redirect('/dashboard')
        # return {
        #     'status':'OK',
        #     'message':'SUCCESSFULLY ADDED IMAGE'
        # }, 200
    session.close()
    return {
        'status':'ERROR',
        'message':'UNPREDICTED ERROR OCCURRED'
    }

@upload_route.route('/doc/add', methods=['POST'])
@login_required
def upload_doc():
    if 'doc' not in request.files:
        # flash('no doc part in request')
        session.close()
        print('no doc part in request')
        return redirect(request.url)
    photo = request.files['doc']
    obj = upload_file(photo, 'DOC')
    if obj['status'] == 'BAD REQUEST':
        print(obj['message'])
        session.close()
        return obj
    if obj['status'] == 'OK':
        print(obj['message'])
        filename = obj['filename']
        info = UploadedFile(filename=filename, file_type='DOC')
        session.add(info)
        session.commit()
        session.close()
        return redirect('/dashboard')
    session.close()
    return {
        'status':'ERROR',
        'message':'UNPREDICTED ERROR OCCURRED'
    }

@upload_route.route('/image/get', methods=['GET'])
def load_images():
    # event_id = request.data['event_id']
    image_records = session.query(UploadedFile).filter_by(file_type='IMAGE').all()
    session.close()
    image_url_array = []
    for image_record in image_records:
        image_url_array.append('/static/photos/'+image_record.file_name)
    return {
        'status':'OK',
        'message':'SUCCESS',
        'array':image_url_array
    }, 200

@upload_route.route('/doc/get', methods=['GET'])
def load_docs():
    # event_id = request.data['event_id']
    # if not Event.query.filter_by(id=event_id).first():
    #     return {
    #         'status':'BAD REQUEST',
    #         'message':'EVENT DOES NOT EXIST'
    #     }
    doc_records = session.query(UploadedFile).filter_by(file_type='DOC').all()
    session.close()
    doc_url_array = []
    for doc_record in doc_records:
        doc_url_array.append(doc_record.file_name)
    return {
        'status':'OK',
        'message':'SUCCESS',
        'array':doc_url_array
    }, 200
