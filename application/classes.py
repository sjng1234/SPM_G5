from re import L
from flask import Blueprint, request, jsonify

from .models import Class
from .extensions import db

classes = Blueprint('class', __name__, url_prefix="/classes")

@classes.route("/")
def class_index():
    return "View Classes"

# Create
@classes.route('/addClass', methods= ["POST"])
def insert():
    try:
        if request.content_type == "application/json":
            post_data = request.get_json()
            new_class = Class(**post_data)
            db.session.add(new_class)
            db.session.commit()
            return jsonify("Successfully created a new class!")
        return jsonify("Something went wrong!")
    except Exception:
        return jsonify({
            "Error Message": "An error has occured when adding class, please try again"
        }), 404

@classes.route("/getAll", methods=["GET"])
def getAll():
    all_books = Class.query.all()
    data = [i.to_dict() for i in all_books]
    return jsonify(data)

@classes.route("/updateClass/<course_id>/<class_id>", methods=["GET"])
def update_class_detail(course_id, class_id):
    try:
        record = Class.query.get((course_id, class_id))
        return jsonify(record)
    except:
        return "Error"