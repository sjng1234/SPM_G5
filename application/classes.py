from re import L
from flask import Blueprint, request, jsonify

from .models import Classes
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
            new_class = Classes(**post_data)
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
    all_books = Classes.query.all()
    count = Classes.query.count()

    return jsonify({
        "count": count,
        "data" : [i.to_dict() for i in all_books]
        })

# Get One
@classes.route("/getOne/<courid>/<classid>", methods=["GET"])
def get_classes_from_course(courid, classid):
    try:
        record = Classes.query.filter_by(course_id = courid, class_id = classid)
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
        record = Classes.query.filter_by(course_id = courid, class_id = classid).first()
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

# DELETE
@classes.route("/delete/<courid>/<cid>", methods = ["DELETE"])
def delete_chapter(courid, cid):
    try:
        record = Classes.query.filter_by(course_id = courid, class_id = cid).first()
        db.session.delete(record)
        db.session.commit()
        return jsonify("Class deleted from Course!")
    except Exception:
        return jsonify({
            "Message": "Class not found in Course, delete not successful."
        }), 404