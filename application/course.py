from flask import Blueprint, request, jsonify

from .models import Course
from .extensions import db

course = Blueprint('course', __name__, url_prefix="/course")

@course.route('/')
def todo_index():
    return "View Courses"

# Create
@course.route('/addCourse',methods = ['POST'])
def insert():
    try:
        if request.content_type == 'application/json':
            post_data = request.get_json()
            new_course = Course(**post_data)
            db.session.add(new_course)
            db.session.commit()
            return jsonify("Successfully posted!")
        return jsonify("Oops something went wrong!")
    except Exception:
        return jsonify({
            "Error Message": "An error occured in adding, please try again"
        }), 404

# Read
@course.route('/getAll',methods = ['GET'])
def return_course():
    all_books = Course.query.all()
    print(all_books)
    print(type(all_books[0]))
    data = [i.to_dict() for i in all_books]
    return jsonify(data)

@course.route('/getCourse/<id>',methods = ['GET'])
def return_get_course_detail(id):
    print(id)
    try:
        data = Course.query.get(id)
        return jsonify(data.to_dict())
    except Exception:
        return jsonify({
            "Error Message": "Course with that ID doesn't exists!"
        }),404
# Update
@course.route('/updateCourse/<id>',methods=['PUT'])
def update_course_detail(id):
    try:
        record = Course.query.get(id)
        if request.content_type == 'application/json':
            put_data = request.get_json()
            course_name = put_data.get('course_name')
            course_description = put_data.get('course_description')
            course_creator_id = put_data.get('course_creator_id')
            date_created = put_data.get('date_created')
            if 'id' in put_data:
                record.id = put_data.get('id')
            record.course_name = course_name
            record.course_description = course_description
            record.course_creator_id = course_creator_id
            record.date_created = date_created
            db.session.commit()
            return jsonify('Updated!')
        else:
            raise Exception
    except Exception:
        return jsonify({
            "message": "Enter Valid JSON request body or a valid id for database"
        }),404
        
# Delete
@course.route('/deleteCourse/<id>', methods=['DELETE'])
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