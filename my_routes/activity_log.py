import datetime as datetime
from models import ActivityLog
from connection import DatabaseHandler

session = DatabaseHandler.connect_to_database()

activity_types = ['added event', 'added photo', 'removed photo', 'added document', 'removed document', 'added result', 'added fest', 'added person']

def activity_performed(activity_type, change_time, username, file_id=None, event_id=None):
    info = ActivityLog(change_time=change_time, user=username, file_id=file_id, event_id=event_id, activity_type=activity_type)
    session.add(info)
    session.commit()
    return {
        'status':'OK',
        'message':'SUCCESSFULLY ADDED ACTIVITY LOG'
    }, 200
