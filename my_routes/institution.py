from flask import request, redirect, flash
from flask_login import login_required
from models import Institution
from connection import DatabaseHandler
from . import institute
import config as config
session = DatabaseHandler.connect_to_database()

@institute.route('/get', methods=['GET'])
# @login_required
def get_institutions():
    colleges = session.query(Institution).all()
    session.close()
    college_json_array = []
    for college in colleges:
        user_json = {
            'college_name':college.name,
            'college_short':college.short,
            'college_id':college.id
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
    try:
        session.commit()
    except:
        session.rollback()
        flash(config.UNEXPECTED_ERROR)
    finally:
        session.close()
    return redirect('/dashboard')

@institute.route('/get/<int:id>', methods=['GET'])
def get_institution(id):
    college = session.query(Institution).filter_by(id=id).first()
    session.close()
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
