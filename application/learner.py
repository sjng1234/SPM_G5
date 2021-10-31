from flask import Blueprint, json, request, jsonify

from .models import User, Learner, Admin, Trainer, Qualifications, Learner_Enrolment, Material_Completion_Status, Quiz_Results
from .extensions import db

learner = Blueprint('learner', __name__,url_prefix='/learner')

@learner.route('/', methods=['GET'])
def test_root_user_route():
    return "learner root route"

# Get learner's all enrolled class
@learner.route('/getEnrolledClasses/<learner_id>', methods=['GET'])
def get_learner_enrolled_classes(learner_id):
    try:
        enrolled_classes = Learner.query.get(learner_id).classes.all()
        all_enrolled_classes = [i.to_dict() for i in enrolled_classes]
        return jsonify(all_enrolled_classes)
    except Exception as e:
        return jsonify({"Error Message": str(e)}),400

# Get learner's all quiz_results
@learner.route('/getAllQuizResults/<learner_id>', methods=['GET'])
def get_quiz_results_all(learner_id):
    try:
        quiz_results = Learner.query.get(learner_id).quiz_results.all()
        all_quiz_results = [i.to_dict() for i in quiz_results]
        return jsonify(all_quiz_results)
    except Exception as e:
        return jsonify({"Error Message": str(e)}),400

# Get learner's specific quiz_results
@learner.route('/getAllQuizResults/<learner_id>/<quiz_id>', methods=['GET'])
def get_quiz_results_one(learner_id,quiz_id):
    try:
        quiz_result = Learner.query.get(learner_id).quiz_results.filter_by(quiz_id=quiz_id).first()
        return jsonify(quiz_result.to_dict())
    except Exception as e:
        return jsonify({"Error Message": str(e)}),400
    
# Learner Enrol in a class
@learner.route('/enrol',methods=['PUT'])
def enrol():
    try: 
        if request.content_type == 'application/json':
            post_data = request.get_json()
            new_learner_enrolment = Learner_Enrolment(**post_data)
            db.session.add(new_learner_enrolment)
            db.session.commit()
            return jsonify("Successfully Enrolled!")
    except Exception as e:
        return jsonify({"Error Message": str(e)}),400