from flask import Blueprint, json, request, jsonify

from .models import User, Learner, Admin, Trainer, Qualifications, Learner_Enrolment, Material_Completion_Status
from .extensions import db

user = Blueprint("user", __name__, url_prefix="/user")

# user root
@user.route("/", methods=["GET"])
def test_root_user_route():
    return "user root route"

# Create
@user.route("/create", methods=["POST"])
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

# GETALL
@user.route("/getAll", methods = ["GET"])
def get_all():
    record = User.query.all()
    result = [i.to_dict() for i in record]
    return jsonify(result)