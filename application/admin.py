from flask import Blueprint, json, request, jsonify

from .models import User, Learner, Admin, Trainer, Qualifications, Learner_Enrolment, Material_Completion_Status, Quiz_Results
from .extensions import db

admin = Blueprint("user", __name__, url_prefix="/admin")

# user root
@admin.route("/", methods=["GET"])
def test_root_user_route():
    return "admin root route"

# Get Admin's Details
@admin.route('/<admin_id>', methods=['GET'])
def get_learner_details(admin_id):
    try:
        user = User.query.get(admin_id)
        if user.user_type != "admin":
            raise Exception("User is not an admin")
        else:
            return jsonify(user.to_dict())
    except Exception as e:
        print(str(e))
        return jsonify({"Error Message": 'Admin Not Found'}), 400

# Create User
@admin.route("/create", methods=["POST"])
def create_user():
    try:
        if request.content_type == "application/json":
            data = request.get_json()
            user_type = data.get("user_type").lower()
            if user_type not in ["learner", "trainer", "admin"]:
                raise Exception("Invalid user type")
            else:
                data.pop("user_type");
                if user_type == "learner":
                    user = Learner(**data)
                elif user_type == "trainer":
                    user = Trainer(**data)
                elif user_type == "admin":
                    user = Admin(**data)
                db.session.add(user)
                db.session.commit()
            return jsonify({"message": "User created successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400


# Create Class [To be Discussed]

# GETALL
@admin.route("/getAll", methods = ["GET"])
def get_all():
    record = User.query.all()
    result = [i.to_dict() for i in record]
    return jsonify(result)

# Get All instructors qualification
@admin.route("/getAllInstructorsQualification", methods = ["GET"])
def get_all_instructors_qualification():
    record = Qualifications.query.all()
    result = [i.to_dict() for i in record]
    return jsonify(result)

# Get All Qualified Trainer to teach a specific course
@admin.route("/<id>/getAllQualifiedTrainer", methods = ["GET"])
def get_course_qualified_trainers(id):
    try:
        record = Qualifications.query.filter_by(course_id = id).all()
        result = [i.to_dict() for i in record]
        return jsonify(result)
    except Exception as e:
        print(str(e))
        return jsonify({"Error Message":"Please Enter a valid Course ID"}), 400

# Get All Learners Quiz Results
@admin.route("/getAllLearnersQuizResults", methods = ["GET"])
def get_all_learners_quiz_results():
    record = Quiz_Results.query.all()
    result = [i.to_dict() for i in record]
    return jsonify(result)

# Get All Learners Material Completion Status
@admin.route("/getAllLearnersMaterialCompletionStatus", methods = ["GET"])
def get_all_learners_material_completion_status():
    record = Material_Completion_Status.query.all()
    result = [i.to_dict() for i in record]
    return jsonify(result)

# Get All Learners Enrolment
@admin.route("/getAllLearnersEnrolment", methods = ["GET"])
def get_all_learners_enrolment():
    record = Learner_Enrolment.query.all()
    result = [i.to_dict() for i in record]
    return jsonify(result)

