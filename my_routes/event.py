import datetime as datetime
from flask import request
from flask_login import login_required
from models import Event, Fest
from connection import DatabaseHandler
from . import events

session = DatabaseHandler.connect_to_database()
@events.route('/<int:year>/add', methods=['POST'])
@login_required
def add_event(year):
    req_fest = Fest.query.filter_by(year=year).first()
    if not req_fest:
        return {
            'status':'BAD REQUEST',
            'message':'NO SUCH FEST'
        }, 201
    name = request.data['name']
    # day = request.data['day']
    day = datetime.datetime.strptime(request.data['day'], '%Y-%m-%d').date()
    start_time = datetime.datetime.strptime(request.data['start_time'], '%H:%M').time()
    end_time = datetime.datetime.strptime(request.data['end_time'], '%H:%M').time()
    venue = request.data['venue']
    info = Event(fest=year, name=name, day=day, start_time=start_time, end_time=end_time, venue=venue)
    print
    session.add(info)
    session.commit()
    return {
        'status':'OK',
        'message':'SUCCESSFULLY ADDED EVENT',
    }, 200

@events.route('/<int:year>/get', methods=['GET'])
def get_events(year):
    all_events = Event.query.filter_by(fest=year).all()
    event_json_array = []
    for each_event in all_events:
        event_json_array.append({
            'year':each_event.fest,
            'name':each_event.name,
            'day':each_event.day,
            'start_time':str(each_event.start_time),
            'end_time':str(each_event.end_time),
            'venue':each_event.venue,
            'id':each_event.id
        })
    return {
        'status':'OK',
        'message':'SUCCESS',
        'array':event_json_array
    }, 200

@events.route('/<int:year>/get/<int:id>', methods=['GET'])
def get_event(year, id):
    event = Event.query.filter_by(fest=year, id=id).first()
    if not event:
        return {
            'status':'BAD REQUEST',
            'message':'NO SUCH FEST'
        }, 201
    event_json = {
        'year':event.fest,
        'name':event.name,
        'day':event.day,
        'start_time':str(event.start_time),
        'end_time':str(event.end_time),
        'venue':event.venue,
        'id':event.id
    }
    print(str(event.day))
    return {
        'status':'OK',
        'message':'SUCCESS',
        'event':event_json
    }, 200
