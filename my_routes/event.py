import datetime as datetime
from flask import request, redirect
from flask_login import login_required
from models import Event, Fest
from connection import DatabaseHandler
from . import events

session = DatabaseHandler.connect_to_database()
@events.route('/<int:year>/add', methods=['POST'])
# @login_required
def add_event(year):
    req_fest = session.query(Fest).filter_by(year=year).first()
    if not req_fest:
        session.close()
        return {
            'status':'BAD REQUEST',
            'message':'NO SUCH FEST'
        }, 201
    name = request.data['name']
    venue = request.data['venue']
    # day = request.data['day']
    info = Event(fest=year, name=name, venue=venue)
    session.add(info)
    try:
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()
    # return redirect('/dashboard')
    return {
        'status':'OK',
        'message':'SUCCESSFULLY ADDED EVENT',
    }, 200

@events.route('/<int:year>/get', methods=['GET'])
def get_events(year):
    all_events = session.query(Event).filter_by(fest=year).all()
    event_json_array = []
    for each_event in all_events:
        event_json_array.append({
            'year':each_event.fest,
            'name':each_event.name,
            'id':each_event.id
        })
    session.close()
    return {
        'status':'OK',
        'message':'SUCCESS',
        'array':event_json_array
    }, 200

@events.route('/<int:year>/get/<int:id>', methods=['GET'])
def get_event(year, id):
    event = session.query(Event).filter_by(fest=year, id=id).first()
    session.close()
    if not event:
        return {
            'status':'BAD REQUEST',
            'message':'NO SUCH FEST'
        }, 201
    event_json = {
        'year':event.fest,
        'name':event.name,
        'id':event.id
    }
    # print(str(event.day))
    return {
        'status':'OK',
        'message':'SUCCESS',
        'event':event_json
    }, 200
