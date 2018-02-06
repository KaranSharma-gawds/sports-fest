import config as config
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, UniqueConstraint, create_engine, Date, Time, TIMESTAMP
from sqlalchemy import Integer, ForeignKey, String, TypeDecorator, Unicode, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import BLOB
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from enum import Enum
app = FlaskAPI(__name__)
# from __init__ import app
db = SQLAlchemy(app)
engine = create_engine(config.sqlite['CREATE_ENGINE_URL'], echo=True)
DeclarativeBase = declarative_base(engine)
metadata = DeclarativeBase.metadata

def  _fk_pragma_on_connect(dbapi_con, con_record):
    dbapi_con.execute('pragma foreign_keys=ON')

event.listen(engine, 'connect', _fk_pragma_on_connect)

class Institution(DeclarativeBase):
    __tablename__ = 'institution'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200))
    short = Column(String(20))
    def __init__(self, name=None, short=None):
        self.name = name
        self.short = short
    def __repr__(self):
        return self.id

class User(DeclarativeBase, UserMixin):
    __tablename__ = 'user'
    username = Column(String(200), primary_key=True)
    pwhash = Column(String(200))
    institution = Column(String(200), ForeignKey('institution.id'))
    def __init__(self, username=None, institution=None, password=None):
        self.institution = institution
        self.username = username
        self.pwhash = generate_password_hash(password)
    def __repr__(self):
        return self.username
    def check_password(self, password):
        return check_password_hash(self.pwhash, password)

class Person(DeclarativeBase):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    institution = Column(Integer, ForeignKey('institution.id'))
    designation = Column(String(100))
    role = Column(String(100))
    contact_no = Column(Integer)
    email_id = Column(String(200))
    image_url = Column(String(200))
    def __init__(self, name=None, institution=None, designation=None, role=None, contact_no=None, email_id=None, image_url=None):
        self.name = name
        self.institution = institution
        self.designation = designation
        self.role = role
        self.contact_no = contact_no
        self.email_id = email_id
        self.image_url = image_url
    def __repr__(self):
        return self.id

class Fest(DeclarativeBase):
    __tablename__ = 'fest'
    year = Column(Integer, primary_key=True)
    host = Column(String, ForeignKey('institution.id'))
    no_of_days = Column(Integer)
    def __init__(self, year=None, no_of_days=None, host=None):
        self.year = year
        self.host = host
        self.no_of_days = no_of_days
    def __repr__(self):
        return self.year

class Event(DeclarativeBase):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fest = Column(Integer, ForeignKey('fest.year'))
    name = Column(String(200))
    day = Column(Integer)
    start_time = Column(Time)
    end_time = Column(Time)
    venue = Column(String(200))
    def __init__(self, fest=None, name=None, day=None, start_time=None, end_time=None, venue=None):
        self.fest = fest
        self.name = name
        self.day = day
        self.start_time = start_time
        self.end_time = end_time
        self.venue = venue
    def __repr__(self):
        return self.id

class Result(DeclarativeBase):
    __tablename__ = 'result'
    event_id = Column(Integer, ForeignKey('event.id'), primary_key=True)
    first_name = Column(String(100))
    first_institution = Column(Integer, ForeignKey('institution.id'))
    second_name = Column(String(100))
    second_institution = Column(Integer, ForeignKey('institution.id'))
    third_name = Column(String(100))
    third_institution = Column(Integer, ForeignKey('institution.id'))
    def __init__(self, event_id=None, first_name=None, first_institution=None, second_name=None, second_institution=None, third_institution=None, third_name=None):
        self.first_institution = first_institution
        self.first_name = first_name
        self.second_institution = second_institution
        self.second_name = second_name
        self.third_institution = third_institution
        self.third_name = third_name
        self.event_id = event_id
    def __repr__(self):
        return self.id

class UploadedFile(DeclarativeBase):
    __tablename__ = 'uploaded_file'
    file_id = Column(Integer, primary_key=True, autoincrement=True)
    file_name = Column(String)
    event_id = Column(String(200), ForeignKey('event.id'))
    def __init__(self, filename=None, event_id=None):
        self.event_id = event_id
        self.file_name = filename
    def __repr__(self):
        return self.photo_id

#activity-type(Enum)
class ActivityLog(DeclarativeBase):
    __tablename__ = 'activity-log'
    id = Column(Integer, primary_key=True, autoincrement=True)
    change_time = Column(TIMESTAMP)
    user = Column(String(200), ForeignKey('user.username'))
    file = Column(Integer, ForeignKey('uploaded_file.file_id'))
    event_id = Column(Integer, ForeignKey('event.id'))
    activity_type = Column(db.Enum(config.ActivityType))
    def __init__(self, change_time=None, user=None, activity_type=None, event_id=None, file_id=None):
        self.change_time = change_time
        self.user = user
        self.activity_type = activity_type
        self.file = file_id
        self.event_id = event_id
    def __repr__(self):
        return self.id

metadata.create_all()
