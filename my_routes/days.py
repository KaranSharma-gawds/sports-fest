from flask import request, redirect
from flask_login import login_required
from models import Event, Day
from connection import DatabaseHandler
from .upload_file import upload_file
from . import day

session = DatabaseHandler.connect_to_database()
@day.route('/<int:event_id>/get', methods=['GET'])
def get_days_by_event(event_id):
    event = Event.query.filter_by(id=event_id).first()
    if not event:
        return{
            'status':'BAD REQUEST',
            'message':'NO SUCH EVENT'
        }, 400
    days = Day.query.filter_by(event_id=event_id).all()
    result = []
    # ids = []
    for each_day in days:
        result.append({
            'name':each_day.name,
            'id':each_day.id
        })
        # ids.append(each_day.id)
    return {
        'status':'OK',
        'message':'SUCCESSFULLY RECIEVED RESULT',
        'array':result,
        # 'ids':ids
    }

@day.route('/get/<int:day_id>', methods=['GET'])
def get_day_by_id(day_id):
    day = Day.query.filter_by(id=day_id).first()
    if not day:
        return {
            'status':'OK',
            'message':'NO SUCH DAY YET',
            'result_pdf':None,
            'fixture_pdf':None,
            'name':None,
            'id':None
        }
    return {
        'status':'OK',
        'message':'SUCCESSFULLY RECIEVED DAY INFORMATION',
        'result_pdf':day.result_pdf,
        'fixture_pdf':day.schedule_pdf,
        'name':day.name,
        'id':day.id
    }

@day.route('/<int:event_id>/add', methods=['POST'])
# @login_required
def add_blank_day(event_id):
    name = request.data['name']
    info = Day(event_id=event_id, name=name, result_pdf=None, schedule_pdf=None)
    session.add(info)
    session.commit()
    # return redirect('/dashboard')
    return {
        'status':'OK'
    }
@day.route('/upload/result/<int:day_id>', methods=['POST', 'GET'])
def upload_result(day_id):
    if request.method == 'GET':
        return render_template('upload_day_result.html', url=url, filetype='doc')
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
        # info = UploadedFile(filename=filename, file_type='DOC')
        my_day = Day.query.filter_by(id=day_id).first()
        my_day.result_pdf = filename
        session.add(my_day)
        session.commit()
        return redirect('/dashboard')
    return {
        'status':'ERROR',
        'message':'UNPREDICTED ERROR OCCURRED'
    }