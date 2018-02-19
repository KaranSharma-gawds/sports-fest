from flask import Blueprint, render_template
from flask_login import login_required
sports = Blueprint('sports', __name__)
@sports.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@sports.route('/signin', methods=['GET'])
def signin():
    return render_template('login.html')

@sports.route('/organisers', methods=['GET'])
def organisers():
    return render_template('organisers.html')

@sports.route('/gallery', methods=['GET'])
def gallery():
    return render_template('gallery.html')

@sports.route('/event', methods=['GET'])
def event():
    return render_template('event.html')

@sports.route('/notifications', methods=['GET'])
def notifications():
    return render_template('notifications.html')

@sports.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@sports.route('/upload/image', methods=['GET'])
@login_required
def upload_image():
    return render_template('upload-image.html', filetype='photo', url='/api/upload/image/add')

@sports.route('/upload/doc', methods=['GET'])
@login_required
def upload_doc():
    return render_template('upload-file.html', filetype='doc', url='/api/upload/doc/add')

@sports.route('/person/add', methods=['GET'])
@login_required
def add_person():
    return render_template('add_person.html', filetype='photo', url='/api/people/add')

@sports.route('/result/add', methods=['GET'])
@login_required
def add_result():
    return render_template('resultupload.html', filetype='photo', url='/api/result/add')

@sports.route('/institute/add', methods=['GET'])
@login_required
def add_institute():
    return render_template('addinsti.html', filetype='photo', url='/api/institute/add')

@sports.route('/day/add', methods=['GET'])
@login_required
def add_day():
    return render_template('add_day.html', filetype='doc', url='/api/<int:event_id>/add')

@sports.route('/daily-fix/add', methods=['GET'])
# @login_required
def add_daily_fix():
    return render_template('add_fix.html', filetype='doc', url='/api/upload/fixture/<int:day_id>')

@sports.route('/daily-result/add', methods=['GET'])
# @login_required
def add_daily_result():
    return render_template('add_result.html', filetype='doc', url='/api/upload/result/<int:day_id>')

@sports.route('/something', methods=['GET'])
def something():
    return render_template('images.html')

@sports.route('/schedule-and-result', methods=['GET'])
def s_and_r():
    return render_template('scheduleandresult.html')