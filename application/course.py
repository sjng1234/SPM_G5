from flask import Blueprint, request, jsonify

from .models import Course
from .extensions import db

course = Blueprint('course', __name__, url_prefix="/course")

@course.route('/')
def todo_index():
    return "View Courses"

@course.route('/getAll',methods = ['GET'])
def return_course():
    all_books = db.session.query(Course.course_id,Course.title,Course.course_description).all()
    data = [dict(i) for i in all_books]
    return jsonify(data)

@course.route('/getCourse/<id>',methods = ['GET'])
def return_get_course_detail(id):
    data = db.session.query(Course.course_id,Course.title,Course.course_description).filter(Course.course_id == id).first()
    return jsonify(dict(data))
