from flask import request, redirect, render_template
from flask_login import login_required
from models import Person
from connection import DatabaseHandler
import os, config as config
from .upload_file import upload_file
from . import people

session = DatabaseHandler.connect_to_database()

@people.route('/get', methods=['GET'])
def get_people():
    all_people = Person.query.all()
    people_json_array = []
    for person in all_people:
        people_json_array.append({
            'name':person.name,
            'institution':person.institution,
            'designation':person.designation,
            'role':person.role,
            'contact_no':person.contact_no,
            'email_id':person.email_id,
            'image_url':'photos/'+person.image_url,
            'id':person.id
        })
    if people_json_array.count == 0:
        return {
            'status':'BAD REQUEST',
            'message':'NO PEOPLE ADDED YET'
        }, 201
    return {
        'status':'OK',
        'message':'SUCCESS',
        'array':people_json_array
    }, 200

@people.route('/add', methods=['GET','POST'])
@login_required
def add_person():
    if request.method == 'POST':
        if 'photo' not in request.files:
            # flash('no photo part in request')
            print('no photo part in request')
            return redirect(request.url)
        photo = request.files['photo']
        name = request.data['name']
        role = request.data['role']
        email_id = request.data['email_id']
        contact_no = request.data['contact_no']
        institution = request.data['institution']
        designation = request.data['designation']
        obj = upload_file(photo, 'IMG')
        if obj['status'] == 'BAD REQUEST':
            print(obj['message'])
            return obj
        if obj['status'] == 'OK':
            print(obj['message'])
            filename = obj['filename']
            # upload_time = obj['upload_time']
            info = Person(name=name, institution=institution, designation=designation, role=role, \
                            email_id=email_id, contact_no=contact_no, image_url=filename)
            session.add(info)
            session.commit()
            return {
                'status':'OK',
                'message':'SUCCESSFULLY ADDED PERSON'
            }
        return {
            'status':'ERROR',
            'message':'UNPREDICTED ERROR OCCURRED'
        }
    else:
        return render_template('add_person.html', filetype='photo', url=request.url)
