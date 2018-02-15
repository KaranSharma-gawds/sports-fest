import datetime as datetime
from flask import request
from flask_login import login_required
from models import Event, Fest, Result
from connection import DatabaseHandler
from . import event_result

session = DatabaseHandler.connect_to_database()

@event_result.route('/get/<int:event_id>', methods=['GET'])
def get_result(event_id):
    # event = request.data['event']
    result = Result.query.filter_by(event_id=event_id).first()
    if not result:
        print('------------------no result uploaded yet---------------')
        return {
            'status':'OK',
            'message':'SUCCESS',
            'result':None
        }
    result_json = {
        'event_id':result.event_id,
        'first_name':result.first_name,
        'first_institution':result.first_institution,
        'second_name':result.second_name,
        'second_institution':result.second_institution,
        'third_name':result.third_name,
        'third_institution':result.third_institution
    }
    return {
        'status':'OK',
        'message':'SUCCESS',
        'result':result_json
    }, 200

@event_result.route('/add', methods=['POST'])
@login_required
def add_result():
    event = request.data['event']
    first_name = request.data['first_name']
    first_institution = request.data['first_institution']
    second_name = request.data['second_name']
    second_institution = request.data['second_institution']
    third_name = request.data['third_name']
    third_institution = request.data['third_institution']
    if not Event.query.filter_by(id=event).first():
        return {
            'status':'BAD REQUEST',
            'message':'EVENT DOES NOT EXIST'
        }
    info = Result(event_id=event, first_name=first_name, first_institution=first_institution, \
                    second_name=second_name, second_institution=second_institution, third_name=third_name, \
                    third_institution=third_institution)
    session.add(info)
    session.commit()
    return {
        'status':'OK',
        'message':'SUCCESSFULLY ADDED RESULT'
    }, 200
