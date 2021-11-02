from flask import Blueprint, request, jsonify
import datetime

from .models import Course
from .extensions import db

course = Blueprint('course', __name__, url_prefix="/course")

@course.route('/')
def todo_index():
    return "View Courses"

# Create
@course.route('/add',methods = ['POST'])
def insert():
    try:
        if request.content_type == 'application/json':
            post_data = request.get_json()
            post_data['date_created']=datetime.datetime.now()
            new_course = Course(**post_data)
            db.session.add(new_course)
            db.session.commit()
            return jsonify("Successfully posted!")
        return jsonify("Oops something went wrong with the JSON script!")
    except Exception as e:
        return jsonify({
            "Error Message": str(e)
        }), 404

# Read
@course.route('/getAll',methods = ['GET'])
def return_course():
    all_books = Course.query.all()
    data = [i.to_dict() for i in all_books]
    return jsonify(data)

@course.route('/getCourse/<id>',methods = ['GET'])
def return_get_course_detail(id):
    try:
        data = Course.query.get(id)
        return jsonify(data.to_dict())
    except Exception:
        return jsonify({
            "Error Message": "Course with that ID doesn't exists!"
        }),404

# Read (Get all classes of a course)   
@course.route('/getCourse/<id>/getAllClasses',methods = ['GET'])
def return_get_course_classes(id):
    try:
        data = Course.query.get(id)
        classes = data.classes.all() # Query All Classes for the Specific Course (Syntax: <queried_data>.<relationship>.all())
        allClasses = [i.to_dict() for i in classes]
        return jsonify(allClasses)
    except Exception:
        return jsonify({
            "Error Message": "Course with that ID doesn't exists!"
        }),404
        
# Update
@course.route('/update/<id>',methods=['PUT'])
def update_course_detail(id):
    try:
        record = Course.query.get(id)
        
        if request.content_type == 'application/json':
            put_data = request.get_json()
            name = put_data.get('course_name')
            description = put_data.get('course_description')
            creator_id = put_data.get('course_creator_id')
            created = put_data.get('date_created')
            if 'id' in put_data:
                record.id = put_data.get('id')
            setattr(record, "course_name", name)
            setattr(record, "course_description", description)
            setattr(record, "course_creator_id", creator_id)
            setattr(record, "date_created", created)
            db.session.commit()
            return jsonify('Updated!')
        return jsonify("Something is wrong with the JSON script!")
    except Exception:
        return jsonify({
            "message": "Enter Valid JSON request body or a valid id for database"
        }),404
        
# Delete
@course.route('/delete/<id>', methods=['DELETE'])
def delete_Todo_Item(id):
    try:
        record = Course.query.get(id)
        db.session.delete(record)
        db.session.commit()
        return jsonify('Deleted')
    except Exception:
        return jsonify({
            "message": "ToDo ID not found in database."
        }), 404