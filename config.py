import os
from enum import Enum

DB_PATH = os.path.join(os.path.dirname(__file__), 'sports.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(DB_PATH)
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = True
HOST = '0.0.0.0'
PORT = 8080
SECRET_KEY = 'suck my dick'
UNEXPECTED_ERROR = 'Unexpected error occured, did you put in all the values?'
PHOTOS_UPLOAD_FOLDER = 'static/photos'
DOCUMENTS_UPLOAD_FOLDER = os.path.join('static','documents') #'static/documents'
ALLOWED_PHOTO_EXTENTIONS = set(['jpg', 'jpeg', 'png'])
ALLOWED_DOCUMENT_EXTENTIONS = set(['pdf', 'docx', 'xlsx', 'odt', 'doc', 'txt', 'rtf', 'PDF', 'DOC', 'DOCX', 'XLSX', 'ODT', 'RTF', 'TXT'])
class ActivityType(Enum):
    ADDED_EVENT = 1
    ADDED_PHOTO = 2
    ADDED_DOCUMENT = 3
    ADDED_RESULT = 4
    ADDED_FEST = 5
    ADDED_PERSON = 6

sqlite = {
    'CREATE_ENGINE_URL': 'sqlite:///{}'.format(DB_PATH)
}
