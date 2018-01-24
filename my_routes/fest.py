from flask import request
from flask_login import login_required
from models import Fest
from connection import DatabaseHandler
from . import sports_fest

session = DatabaseHandler.connect_to_database()

@sports_fest.route('/get', methods=['GET'])
def get_all_fests():
    fests = Fest.query.all()
    fest_json_array = []
    for  each_fest in fests:
        fest_json_array.append({
            'year':each_fest.year,
            'host':each_fest.host,
            'no_of_days':each_fest.no_of_days
        })
    if fest_json_array.count == 0:
        return {
            'status':'BAD REQUEST',
            'message':'NO FESTS ADDED YET'
        }, 201
    return {
        'status':'OK',
        'message':'SUCCESS',
        'array':fest_json_array
    }, 200

@sports_fest.route('/add', methods=['GET','POST'])
@login_required
def add_sports_fest():
    if request.method == 'POST':
        year = request.data['year']
        host = request.data['host']
        no_of_days = request.data['no_of_days']
        info = Fest(year=year, host=host, no_of_days=no_of_days)
        session.add(info)
        session.commit() 
        return {
            'status':'OK',
            'message':'SUCCESSFULLY ADDED FEST'
        }, 200
    else:
        return {
            'status':'OK',
            'message':'RUNNING',
        }, 200

@sports_fest.route('/get/<int:year>', methods=['GET'])
def get_fest(year):
    req_fest = Fest.query.filter_by(year=year).first()
    fest_json = {
        'year':req_fest.year,
        'host':req_fest.host,
        'no_of_days':req_fest.no_of_days
    }
    return {
        'status':'OK',
        'message':'SUCCESS',
        'fest':fest_json
    }, 200
