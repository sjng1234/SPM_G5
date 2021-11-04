from re import L
from flask import Blueprint, request, jsonify

from .models import Classes, Course, Trainer, User, Quiz, Quiz_Questions, Quiz_Questions_Options
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
    try:
        classes = Classes.query.all()
        output = []
        for c in classes:
            class_details = c.to_dict()
            trainer_id = class_details['trainer_id']
            course_id = class_details['course_id']
            course_detail = Course.query.get(course_id)
            trainer_id_exist = Trainer.query.get(trainer_id)
            if trainer_id_exist:
                trainer_detail = User.query.get(trainer_id_exist.trainer_id)
                class_details.update(course_detail.to_dict())
                class_details.update(trainer_detail.to_dict())
                output.append(class_details)
                # return jsonify(output)    
            else:
                return jsonify({
                    "Error Message": "Invalid Trainer ID"
                }), 404
        return jsonify(output)
    except Exception:
        return jsonify({
            "Error Message": "An error has occurred when getting classes, please try again"
        }), 404
# Get One 
@classes.route("/get/<id>",methods=["GET"])
def getOne(id):
    try:
        [cour_id,class_id] = id.split("-")
        record = Classes.query.filter_by(class_id=class_id, course_id=cour_id).first().to_dict()
        trainer_id = record['trainer_id']
        course_id = record['course_id']
        course_detail = Course.query.get(course_id)
        trainer_id_exist = Trainer.query.get(trainer_id)
        trainer_detail = User.query.get(trainer_id_exist.trainer_id)
        record.update(course_detail.to_dict())
        record.update(trainer_detail.to_dict())
        return jsonify(record)
    except Exception as e:
        # print(str(e))
        return jsonify({
            "message": "Class not found"
        }),400

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
            
            if creator_id:
                setattr(record, "class_creator_id", creator_id)
            if size:
                setattr(record, "class_size", size)
            if end:
                setattr(record, "end_datetime", end)
            if start:
                setattr(record, "start_datetime", start)
            if tid:
                setattr(record, "trainer_id", tid)

            db.session.commit()
            return jsonify("Successful update of class content!")
        return jsonify("Something is wrong with the JSON script!")
    except Exception:
        return jsonify({
            "message": "Enter Valid JSON request body or a valid id for database"
        }),404

# DELETE
@classes.route("/delete/<id>", methods = ["DELETE"])
def delete_chapter(id):
    try:
        [courid, classid] = id.split("-")
        record = Classes.query.filter_by(course_id = courid, class_id = classid).first()
        db.session.delete(record)
        db.session.commit()
        return jsonify("Class deleted from Course!")
    except Exception:
        return jsonify({
            "Message": "Class not found in Course, delete not successful."
        }), 404
        
# Get Quiz Specifics
@classes.route('/getQuiz/<id>',methods=['GET'])
def get_quiz(id):
    try:
        [courid, classid, quiz_id] = id.split("-")
        record = Quiz.query.filter_by(course_id = courid, class_id = classid, quiz_id=quiz_id).first()
        output = {
            **record.to_dict(),
            "question": []
        }
        question = record.questions.all()
        for q in question:
            q_dict = q.to_dict()
            del q_dict['quiz_id']
            del q_dict['class_id']
            del q_dict['course_id']
            q_dict['options'] = []
            options = q.options.all()
            for o in options:
                o_dict = o.to_dict()
                del o_dict['question_id']
                del o_dict['quiz_id']
                del o_dict['class_id']
                del o_dict['course_id']
                q_dict['options'].append(o_dict)
            output["question"].append(q_dict)
        
        return jsonify(output)
    except Exception as e:
        return jsonify({
            'message': str(e)
        }),400
