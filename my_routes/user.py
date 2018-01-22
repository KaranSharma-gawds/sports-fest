from . import login, login_manager
from flask import request, abort
from models import User, Institution
from connection import DatabaseHandler
from flask_login import login_required

session = DatabaseHandler.connect_to_database()

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

@login_manager.user_loader
def load_user(user_id):
    my_user = User.query.filter_by(username=user_id)
    if not my_user:
        return None
    return my_user

@login.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method=='GET':
        return {
            'status':'SUCCESS',
            'message':'RUNNING'
        }, 200
    user_name = request.data['user_name']
    user = load_user(user_name)
    if not user:
        return {
            'status':'BAD REQUEST',
            'message':'USER DOES NOT EXIST'
        }, 201
    next = request.args.get('next')
    if not is_safe_url(next):
        return abort(400)
    return {
        'status':'SUCCESS',
        'message':'SUCCESSFULLY LOGGED IN'
    }, 200

@login.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return {
        'status':'SUCCESS',
        'message':'SUCCESSFULLY LOGGED OUT'
    }, 200

@login.route('/register', methods=['POST'])
def register():
    user_name = request.data['user_name']
    password = request.data['password']
    institution = request.data['institution']
    user = User.query.filter_by(username=user_name).first()
    if user is not None:
        return {
            'status':'BAD REQUEST',
            'message':'USER ALREADY EXISTS',
            'username': user.username,
            'institution':user.institution
        }, 201
    if not Institution.query.filter_by(id=institution).first():
        return {
            'status':'BAD REQUEST',
            'message':'INSTITUTION DOES NOT EXIST'
        }, 201
    info = User(username=user_name, institution=institution,password=password)
    session.add(info)
    session.commit()
    return {
        'status':'SUCCESS',
        'message':'SUCCESSFULLY REGISTERED'
    }, 200
