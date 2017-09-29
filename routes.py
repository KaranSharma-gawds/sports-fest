import os
import datetime as datetime, time
import config as config
from flask import Blueprint, request, url_for, render_template, redirect, send_file #, flash
from models import NIT, Event, ActivityLog, User, Uploaded_File
from connection import DatabaseHandler
from flask_restful import reqparse
from werkzeug.utils import secure_filename
# from __init__ import app

sports = Blueprint('sports', __name__)
# database_handler = DatabaseHandler()
session = DatabaseHandler.connect_to_database()
# session.execute('Pragma foreign_keys = ON')

@sports.route('/add-nit', methods = ['GET', 'POST'])
def addNit():
    if request.method == 'POST':
        info = NIT(college_name = request.data['college_name'], college_short = request.data['college_short'])
        session.add(info)
        session.commit()
        return {'status':'successfully added NIT'}
    else:
        return {'status':'running'}

@sports.route('/all-nits', methods = ['GET'])
def getNits():
    colleges = NIT.query.all()
    college_json_array = []
    for college in colleges:
        user_json = {'collegename':college.college_name, 'college short':college.college_short, 'college id':college.college_id}
        college_json_array.append(user_json)
    return college_json_array, 200

@sports.route('/add-event', methods = ['GET', 'POST'])
def addEvent():
    if request.method == 'POST':
        addTime = datetime.datetime.now()
        startDate = datetime.datetime.strptime(request.data['start_date'], '%d-%m-%Y').date()
        endDate = datetime.datetime.strptime(request.data['end_date'], '%d-%m-%Y').date()
        startTime = datetime.datetime.strptime(request.data['start_time'], '%H-%M').time()
        endTime = datetime.datetime.strptime(request.data['end_time'], '%H-%M').time()
        username = request.data['username']
        info = Event(event_name = request.data['event_name'], host = request.data['host'], username = username, start_date = startDate, end_date = endDate, start_time = startTime, end_time = endTime, place = request.data['place'], year = request.data['year'])
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
            # username = request.data['username']
            # info = Uploaded_File(upload_time = uploadTime, filename = photo.filename, username = username, event = request.data['event'])
            info = Uploaded_File(upload_time = uploadTime, filename = photo.filename, username = 'naruto', event = '6', )
            session.add(info)
            photo.save(os.path.join(config.PHOTOS_UPLOAD_FOLDER, filename))
            session.commit()
            file = Uploaded_File.query.filter_by(upload_time = uploadTime).first()
            file_id = file.file_id
            return [{'status':'uploaded photo'}, addActivityLog(changeTime = uploadTime, file = file_id, user = 'naruto', eventId = '6', activityType = 'added photo')]
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
            # username = request.data['username']
            # info = Uploaded_File(upload_time = uploadTime, filename = doc.filename, username = username, event = request.data['event'])
            info = Uploaded_File(upload_time = uploadTime, filename = doc.filename, username = 'naruto', event = 'chunin exams', )
            session.add(info)
            doc.save(os.path.join(config.DOCUMENTS_UPLOAD_FOLDER, filename))
            session.commit()
            file = Uploaded_File.query.filter_by(upload_time = uploadTime).first()
            file_id = file.file_id
            return [{'status':'added document'},addActivityLog(changeTime = uploadTime, user = 'naruro', file = file_id, activityType = 'added document')]
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
    exists = Uploaded_File.query.filter_by(event = event_id).all()
    files = []
    for file in exists:
        if file.file_name.rsplit('.', 1)[1].lower() in config.ALLOWED_PHOTO_EXTENTIONS:
            url = os.path.join(config.PHOTOS_UPLOAD_FOLDER, file.file_name)
            files.append(url)
    return {'files':files}
    # if exists:
    #     return send_file(config.HOST + '/' + config.PORT + '/' + config.PHOTOS_UPLOAD_FOLDER + '/' + file_name, attachment_filename = file_name)
    # return {'status':'no such file exists'}