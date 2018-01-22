import os
import datetime as datetime, time
import config as config
from flask import Blueprint, request, url_for, render_template, redirect, send_file #, flash
from models import Institution, Event, ActivityLog, User, UploadedFile, Person, Result, Fest
from connection import DatabaseHandler
from flask_restful import reqparse
from werkzeug.utils import secure_filename
from my_routes.institution import InstitutionRoutes
sports = Blueprint('sports', __name__)
# database_handler = DatabaseHandler()
session = DatabaseHandler.connect_to_database()
# session.execute('Pragma foreign_keys = ON')

@sports.route('/add-institution', methods = ['GET', 'POST'])
def add_institution():
    if request.method == 'POST':
        info = Institution(college_name = request.data['college_name'], college_short = request.data['college_short'])
        session.add(info)
        session.commit()
        return {'status':'successfully added institution'}
    else:
        return {'status':'running'}

#@sports.route('/all-nits', methods = ['GET'])
#def get_institution():
#    InstitutionRoutes.get_institutions()

# def get_institution():
#     colleges = Institution.query.all()
#     college_json_array = []
#     for college in colleges:
#         user_json = {'collegename':college.college_name, 'college short':college.college_short, 'college id':college.college_id}
#         college_json_array.append(user_json)
#     return college_json_array, 200

@sports.route('/add-person', methods = ['GET', 'POST'])
def add_person():
    if request.method == 'POST':
        name = request.data['name']
        institution = request.data['institution']
        designation = request.data['designation']
        role = request.data['role']
        contact_no = request.data['contact no']
        email_id = request.data['email_id']
        if 'photo' not in request.files:
            # flash('no photo part in request')
            print('no photo part in request')
            return redirect(request.url)
        photo = request.files['photo']
        if photo.filename == '':
            # flash('no photo selected')
            print('no photo selected')
            return redirect(request.url)
        if photo and allowedPhoto(photo.filename):
            filename = secure_filename(photo.filename)
            uploadTime = datetime.datetime.now()
            filename = uploadTime + '_' + filename
            photo.save(os.path.join(config.PHOTOS_UPLOAD_FOLDER, filename))
            info = Person(name=name, institution=institution, designation=designation, role = role, contact_no=contact_no, email_id=email_id, image_url=filename)
            session.add(info)
            session.commit()
            addActivityLog(changeTime=uploadTime, user=request.data['username'], activityType='added person', file=None, eventId=request.data['event'])
        return {'status': 'added person'}
    else:
        return {'status':running}

@sports.route('/add-event', methods = ['GET', 'POST'])
def addEvent():
    if request.method == 'POST':
        addTime = datetime.datetime.now()
        day = request.data['day']
        startTime = datetime.datetime.strptime(request.data['start_time'], '%H-%M').time()
        endTime = datetime.datetime.strptime(request.data['end_time'], '%H-%M').time()
        username = request.data['username']
        info = Event(event_name = request.data['event_name'], host = request.data['host'], username = username, day=day, start_time = startTime, end_time = endTime, place = request.data['place'], year = request.data['year'])
        session.add(info)
        session.commit()
        eventId = info.event_id
        return [{'status':'successfully added event'},addActivityLog(user = username, activityType = 'added event', eventId = eventId, changeTime = addTime)]
    else:
        return {'status':'running'}

@sports.route('/all-events', methods = ['GET'])
def allEvents():
    users = Event.query.all()
    user_json_array = []
    for user in users:
        user_json = {
            'event id':user.event_id,
            'event name':user.event_name,
            'start date':user.start_date,
            'end date':user.end_date,
            'host':user.host,
            'username':user.username,
            'start time':str(user.start_time),
            'end time':str(user.end_time),
            'place':user.place,
            'year':user.year
        }
        user_json_array.append(user_json)
    return user_json_array, 200

@sports.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.data['username']
        user = User.query.filter_by(username = username).first()
        if not user:
            return {'status':'invalid username'}
        password = request.data['password']
        if user.checkPassword(password = password):
            return {'status':'valid'}
        return {'status':'invalid password'}
    return render_template('login.html')

@sports.route('/signup', methods = ['GET', 'POST'])
def addUser():
    if request.method == 'POST':
        username = request.data['username']
        casea = User.query.filter_by(username = username).first()
        if casea:
            return {'status':False}
        password = request.data['password']
        info = User(username = username, college_id = request.data['college_id'], password = password)
        session.add(info)
        session.commit()
        return {'status':'successfully added user'}
    else:
        return render_template('signup.html')

@sports.route('/all-users', methods = ['GET'])
def allUsers():
    users = User.query.all()
    user_json_array = []
    for user in users:
        user_json = {'username':user.username, 'college_id':user.college_id}
        user_json_array.append(user_json)
    return user_json_array, 200

def allowedPhoto(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_PHOTO_EXTENTIONS

def allowedDocument(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_DOCUMENT_EXTENTIONS

@sports.route('/upload-photo', methods = ['GET', 'POST'])
def uploadPhoto():
    if request.method == 'POST':
        if 'photo' not in request.files:
            # flash('no photo part in request')
            print('no photo part in request')
            return redirect(request.url)
        photo = request.files['photo']
        if photo.filename == '':
            # flash('no photo selected')
            print('no photo selected')
            return redirect(request.url)
        if photo and allowedPhoto(photo.filename):
            filename = secure_filename(photo.filename)
            uploadTime = datetime.datetime.now()
            filename = uploadTime + '_' + filename
            # username = request.data['username']
            # info = Uploaded_File(upload_time = uploadTime, filename = photo.filename, username = username, event = request.data['event'])
            photo.save(os.path.join(config.PHOTOS_UPLOAD_FOLDER, filename))
            info = Uploaded_File(upload_time = uploadTime, filename = photo.filename, username = 'naruto', event = '7')
            session.add(info)
            session.commit()
            file = Uploaded_File.query.filter_by(upload_time = uploadTime).first()
            file_id = file.file_id
            return [{'status':'uploaded photo'}, addActivityLog(changeTime = uploadTime, file = file_id, user = 'naruto', eventId = '7', activityType = 'added photo')]
    else:
        return render_template('upload-file.html', filetype = 'photo', url = '/upload-photo')

@sports.route('/upload-document', methods=['POST','GET'])
def uploadDocument():
    if(request.method == 'POST'):
        if 'doc' not in request.files:
            # flash('no doc part in request')
            print('no doc part in request')
            return redirect(request.url)
        doc = request.files['doc']
        if doc.filename == '':
            # flash('no doc selected')
            print('no doc selected')
            return redirect(request.url)
        if doc and allowedDocument(doc.filename):
            filename = secure_filename(doc.filename)
            uploadTime = datetime.datetime.now()
            filename = uploadTime + '_' + filename
            # username = request.data['username']
            # info = Uploaded_File(upload_time = uploadTime, filename = doc.filename, username = username, event = request.data['event'])
            doc.save(os.path.join(config.DOCUMENTS_UPLOAD_FOLDER, filename))
            info = Uploaded_File(upload_time = uploadTime, filename = filename, username = 'naruto', event = '7')
            session.add(info)
            session.commit()
            file = Uploaded_File.query.filter_by(upload_time = uploadTime).first()
            file_id = file.file_id
            return [{'status':'added document'},addActivityLog(changeTime = uploadTime, user = 'naruro', file = file_id, activityType = 'added document', eventId = '7')]
    else:
        return render_template('upload-file.html', filetype = 'doc', url = '/upload-document')

def addActivityLog(changeTime = None, user = None, activityType = None, file = None, eventId = None):
    if request.method == 'POST':
        info = ActivityLog(change_time = changeTime, file_id = file, user = user, activity_type = activityType, event = eventId)
        session.add(info)
        session.commit()
        return {'status':'added activity log'}
    else:
        return {'status':'running'}

@sports.route('/activity-logs', methods=['GET'])
def getActivityLogs():
    logs = ActivityLog.query.all()
    log_json_array = []
    for log in logs:
        log_json = {log.user:log.activity_type, 'file_id':log.file, 'on':log.change_time, 'event id':log.event}
        log_json_array.append(log_json)
    return log_json_array, 200

@sports.route('/events-images', methods = ['GET'])
def loadImages():
    return render_template('images.html')

@sports.route('/load-image/<event_id>', methods=['GET'])
def getUrls(event_id):
    files = Uploaded_File.query.filter_by(event = event_id).all()
    urls = []
    for file in files:
        if file.file_name.rsplit('.', 1)[1].lower() in config.ALLOWED_PHOTO_EXTENTIONS:
            url = os.path.join(config.PHOTOS_UPLOAD_FOLDER, file.file_name)
            urls.append(url)
    return {'urls':urls}

@sports.route('/load-images/<image_id>', methods = ['GET'])
def loadImage(image_id):
    file = Uploaded_File.query.get(image_id);
    if file:
        return send_file(os.path.join(config.PHOTOS_UPLOAD_FOLDER, file.file_name), attachment_filename = file.file_name)
    return {'status':'no such file exists'}