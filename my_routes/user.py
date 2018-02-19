from . import login, login_manager
# from urlparse import urlparse, urljoin
try:
    from urllib.parse import urlparse, urljoin
except ImportError:
     from urlparse import urlparse, urljoin
from flask import request, abort, redirect, flash
from models import User, Institution
from connection import DatabaseHandler
from flask_login import login_required, logout_user, current_user, login_user
import config as config
session = DatabaseHandler.connect_to_database()

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

@login_manager.user_loader
def load_user(user_id):
    my_user = session.query(User).filter_by(username=user_id).first()
    print('inside load user')
    if not my_user:
        print('load user returning none')
        return None
    print('load user returning'+str(my_user))
    return my_user

@login.route('/login', methods=['POST'])
def user_login():
    user_name = request.data['user_name']
    user = session.query(User).filter_by(username=user_name).first()
    session.close()
    if not user:
        return {
            'status':'BAD REQUEST',
            'message':'USER DOES NOT EXIST'
        }, 201
    if not user.check_password(request.data['password']):
        return {
            'status':'ERROR',
            'message':'INVALID PASSWORD'
        }
    login_user(user)
    user = load_user(user_name)
    # print("printing user" + user)
    next = request.args.get('next')
    if not is_safe_url(next):
        return abort(400)
    # return redirect('/dashboard', code=300)
    return {
        'status':'OK',
        'message':'SUCCESSFULLY LOGGED IN'
    }, 200

@login.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    session.close()
    return redirect('/signin')
    # return {
    #     'status':'OK',
    #     'message':'SUCCESSFULLY LOGGED OUT'
    # }, 200

@login.route('/register', methods=['POST'])
# @login_required
def register():
    user_name = request.data['user_name']
    password = request.data['password']
    institution = request.data['institution']
    user = session.query(User).filter_by(username=user_name).first()
    if user is not None:
        session.close()
        return {
            'status':'BAD REQUEST',
            'message':'USER ALREADY EXISTS',
            'username': user.username,
            'institution':user.institution
        }, 201
    if not session.query(Institution).filter_by(id=institution).first():
        session.close()
        return {
            'status':'BAD REQUEST',
            'message':'INSTITUTION DOES NOT EXIST'
        }, 201
    info = User(username=user_name, institution=institution,password=password)
    session.add(info)
    try:
        session.commit()
    except:
        session.rollback()
        flash(config.UNEXPECTED_ERROR)
    session.close()
    return redirect('/dashboard')
    # return {
    #     'status':'SUCCESS',
    #     'message':'SUCCESSFULLY REGISTERED'
    # }, 200

# @login.route('/', methods=['GET'])
# def some():
#     user_result = session.query(User).all()
#     session.close()
#     users = []
#     for each_user in user_result:
#         users.append(each_user.username)
#     return {
#         'name':users
#     }