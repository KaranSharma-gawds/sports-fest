import config as config
from sqlalchemy import Column, UniqueConstraint, create_engine, Date, Time, TIMESTAMP
from sqlalchemy import Integer, ForeignKey, String, TypeDecorator, Unicode, Enum, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import BLOB
from werkzeug.security import generate_password_hash, check_password_hash


engine = create_engine(config.sqlite['CREATE_ENGINE_URL'], echo=True)
DeclarativeBase = declarative_base(engine)
metadata = DeclarativeBase.metadata

def  _fk_pragma_on_connect(dbapi_con, con_record):
    dbapi_con.execute('pragma foreign_keys=ON')

event.listen(engine, 'connect', _fk_pragma_on_connect)

class NIT(DeclarativeBase):
    __tablename__ = 'NIT'
    college_id = Column(Integer, primary_key = True, autoincrement = True)
    college_name = Column(String(200))
    college_short = Column(String(20))
    def __init__(self, college_name=None, college_short=None):
        self.college_name = college_name
        self.college_short = college_short
    def repr(self):
        return self.college_name

class Event(DeclarativeBase):
    __tablename__ = 'event'
    event_id = Column(Integer, primary_key=True, autoincrement=True)
    event_name = Column(String(200))
    host = Column(String(200), ForeignKey('NIT.college_id'))
    start_date = Column(Date)
    end_date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)
    place = Column(String(200))
    year = Column(Integer)
    username = Column(String(200), ForeignKey('user.username'))
    def __init__(self, event_name = None, host = None, username = None, start_date = None, end_date = None, start_time = None, end_time = None, place = None, year = None):
        self.event_name = event_name
        self.start_date = start_date
        self.host = host
        self.username = username
        self.end_date = end_date
        self.start_time = start_time
        self.end_time = end_time
        self.place = place
        self.year = year
    def __repr__(self):
        return self.name

class User(DeclarativeBase):
    __tablename__ = 'user'
    username = Column(String(200), primary_key = True)
    pwhash = Column(String(200))
    college_id = Column(String(200), ForeignKey('NIT.college_id'))
    def __init__(self, username = None, college_id = None, password = None):
        self.college_id = college_id
        self.username = username
        self.pwhash = generate_password_hash(password)
    def __repr__(self):
        return self.username
    def checkPassword(self, password):
        return check_password_hash(self.pwhash, password)

class Uploaded_File(DeclarativeBase):
    __tablename__ = 'uploaded_file'
    file_id = Column(Integer, primary_key=True, autoincrement=True)
    file_name = Column(String)
    username = Column(String(200), ForeignKey('user.username'))
    upload_time = Column(TIMESTAMP)
    event = Column(String(200), ForeignKey('event.event_id'))
    def __init__(self, filename = None, username = None, upload_time = None, event = None):
        self.username = username
        self.upload_time = upload_time
        self.event = event
        self.file_name = filename
    def __repr__(self):
        return self.photo_id

#activity-type(Enum)
class ActivityLog(DeclarativeBase):
    __tablename__ = 'activity-log'
    log_id = Column(Integer, primary_key=True, autoincrement=True)
    change_time = Column(TIMESTAMP)
    user = Column(String(200), ForeignKey('user.username'))
    file = Column(Integer, ForeignKey('uploaded_file.file_id'))
    event = Column(Integer, ForeignKey('event.event_id'))
    activity_type = Column(Enum('added event','added photo','removed photo','added document','removed document'))
    def __init__(self, change_time = None, user = None, activity_type = None, event = None, file_id = None):
        self.change_time = change_time
        self.user = user
        self.activity_type = activity_type
        self.file = file_id
        self.event = event
    def __repr__(self):
        return self.id

metadata.create_all()
