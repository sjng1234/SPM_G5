from re import L
from flask import Blueprint, request, jsonify

from .models import Classes, Course, Trainer
from .extensions import db

classes = Blueprint('class', __name__, url_prefix="/classes")

@classes.route("/")
def class_index():
    return "View Classes"

# Create
@classes.route('/add', methods= ["POST"])
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
    classes = Classes.query.all()
    output = []
    for c in classes:
        class_details = c.to_dict()
        trainer_id = class_details['trainer_id']
        course_id = class_details['course_id']
        course_detail = Course.query.get(course_id)
        trainer_detail = Trainer.query.get(trainer_id)
        print(trainer_detail)
        class_details.update(course_detail.to_dict())
        class_details.update(trainer_detail.to_dict())
        output.append(class_details)
    return jsonify(output)


    

# UPDATE
@classes.route("/update/<id>", methods=["PUT"])
def update_class_detail(id):
    try:
        [courid, classid] = id.split("-")
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