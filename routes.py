from flask import Blueprint, render_template
sports = Blueprint('sports', __name__)
@sports.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@sports.route('/signin', methods=['GET'])
def signin():
    return render_template('login.html')

@sports.route('/event', methods=['GET'])
def event():
    return render_template('event.html')

@sports.route('/notifications', methods=['GET'])
def notifications():
    return render_template('notifications.html')

@sports.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')

@sports.route('/upload/image', methods=['GET'])
def upload_image():
    return render_template('upload-file.html', filetype='photo', url='/api/upload/image/add')

@sports.route('/upload/doc', methods=['GET'])
def upload_doc():
    return render_template('upload-file.html', filetype='doc', url='/api/upload/doc/add')

@sports.route('/person/add')
def add_person():
    return render_template('add_person.html', filetype='photo', url='/api/people/add')

