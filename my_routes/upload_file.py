import os
import datetime as datetime
from werkzeug.utils import secure_filename
import config as config

def allowed_photo(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_PHOTO_EXTENTIONS

def allowed_document(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_DOCUMENT_EXTENTIONS

def upload_file(file, file_type):
    if file.filename == '':
        return {
            'status':'BAD REQUEST',
            'message':'NO FILE SELECTED'
        }
    if (file_type == 'IMG' and allowed_photo(file.filename)) or (file_type == 'DOC' and allowed_document(file.filename)):
        filename = secure_filename(file.filename)
<<<<<<< HEAD
        upload_time = datetime.datetime.timestamp(datetime.datetime.now())
        filename = str(upload_time) + '_' + filename
=======
        # upload_time = datetime.datetime.timestamp(datetime.datetime.now())
        # filename = str(upload_time) + '_' + filename
>>>>>>> 58b80612666ab43fcd1d8883960bf00f114b4d2d
        if(file_type == 'IMG'):
            file.save(os.path.join(config.PHOTOS_UPLOAD_FOLDER, filename))
        else:
            file.save(os.path.join(config.DOCUMENTS_UPLOAD_FOLDER, filename))
        return {
            'status':'OK',
            'message':'FILE SAVED',
<<<<<<< HEAD
            'filename':filename,
            'upload_time':upload_time
=======
            'filename':filename
            # 'upload_time':upload_time
>>>>>>> 58b80612666ab43fcd1d8883960bf00f114b4d2d
        }
    else:
        return {
            'status':'BAD REQUEST',
            'message':'INVALID FILE'
        }
