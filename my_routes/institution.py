from flask import request
from flask_login import login_required
from models import Institution
from connection import DatabaseHandler
from . import institute

session = DatabaseHandler.connect_to_database()

# @login_required    #implement when login is completed
@institute.route('/get', methods=['GET'])
def get_institutions():
    colleges = Institution.query.all()
    college_json_array = []
    for college in colleges:
        user_json = {
            'collegename':college.name,
            'college short':college.short,
            'college id':college.id
        }
        college_json_array.append(user_json)
    if not college_json_array:
        return {
            'status':'BAD REQUEST',
            'message':'NO INSTITUTION YET'
        }, 201
    return {
        'status':'OK',
        'message':'SUCCESS',
        'array':college_json_array
    }, 200

@institute.route('/add', methods=['POST'])
@login_required
def add_institution():
    info = Institution(name = request.data['college_name'], short = request.data['college_short'])
    session.add(info)
    session.commit()
    return {
        'status':'OK',
        'message':'SUCCESS',
    }, 200

@institute.route('/get/<int:id>', methods=['GET'])
def get_institution(id):
    college = Institution.query.filter_by(id=id).first()
    if not college:
        return {
            'status':'BAD REQUEST',
            'message':'INSTITUTION DOES NOT EXIST'
        }, 201
    return {
        'status':'OK',
        'message':'SUCCESS',
        'college name':college.name,
        'college short':college.short,
        'college id':college.id
    }, 200
