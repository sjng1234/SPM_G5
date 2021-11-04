from flask import Blueprint, json, request, jsonify

from .models import User, Learner, Admin, Trainer, Qualifications, Learner_Enrolment, Material_Completion_Status, Quiz_Results, Classes
from .extensions import db

trainer = Blueprint("trainer", __name__, url_prefix="/trainer")

@trainer.route("/", methods=["GET"])
def test_trainer():
    return jsonify("Root Trainer Route")

# Trainer Get All His Qualifications
@trainer.route("/getAllQualifications/<id>", methods=["GET"])
def get_qualifications(id):
    try:
        qualifications = Trainer.query.get(id).all_qualified_course
        result = [i.to_dict()['course_id'] for i in qualifications]
        return jsonify(result)
    except Exception as e:
        # print(str(e))
        return jsonify({"Error Message":"Please Enter a Valid Trainer ID"}), 400

# Trainer Get All His Classes
@trainer.route("/getAllClasses/<id>", methods=["GET"])
def get_all_classes(id):
    try:
        classes = Classes.query.filter_by(trainer_id=id).all()
        result = [i.to_dict() for i in classes]
        return jsonify(result)
    except Exception as e:
        # print(str(e))
        return jsonify({"Error Message":"Please Enter a Valid Trainer ID"}), 400
    
# Trainer Update Qualifications
@trainer.route("/updateQualifications", methods=["PUT"])
def add_qualifications():
    try:
        data = request.get_json()
        new_qualification = Qualifications(**data)
        db.session.add(new_qualification)
        db.session.commit()
        return jsonify({"Message": "Qualification added successfully"})
    except Exception as e:
        # print(str(e))
        return jsonify({"Error message": "Invalid Trainer or Course ID"}),400