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
            "Error Message": "An error has occurred when adding class, please try again"
        }), 404

# Get All
@classes.route("/getAll", methods=["GET"])
def getAll():
    all_books = Class.query.all()
    data = [i.to_dict() for i in all_books]
    return jsonify(data)

# Get One
@classes.route("/getOne/<courid>/<classid>", methods=["GET"])
def get_classes_from_course(courid, classid):
    try:
        record = Class.query.filter_by(course_id = courid, class_id = classid)
        result = [i.to_dict() for i in record]
        return jsonify(result)
    except:
        return jsonify({
            "Error Message": "Course is not found, thus there are no registered classes"
        }), 404

# UPDATE
@classes.route("/updateClass/<courid>/<classid>", methods=["PUT"])
def update_class_detail(courid, classid):
    try:
        record = Class.query.filter_by(course_id = courid, class_id = classid).first()
        if request.content_type == "application/json":
            put_data = request.get_json()
            creator_id = put_data.get("class_creator_id")
            size = put_data.get("class_size")
            end = put_data.get("end_datetime")
            start = put_data.get("start_datetime")
            tid = put_data.get("trainer_id")

            setattr(record, "class_creator_id", creator_id)
            setattr(record, "class_size", size)
            setattr(record, "end_datetime", end)
            setattr(record, "start_datetime", start)
            setattr(record, "trainer_id", tid)

            db.session.commit()
            return jsonify("Successful update of class content!")
        return jsonify("Something is wrong with the JSON script!")
    except Exception:
        return jsonify({
            "message": "Enter Valid JSON request body or a valid id for database"
        }),404