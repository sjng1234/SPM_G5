from flask import Blueprint, request, jsonify

from .models import Quiz_Questions, Quiz_Questions_Options
from .extensions import db

quiz_questions = Blueprint('quiz_questions', __name__, url_prefix="/quiz_questions")

@quiz_questions.route('/')
def todo_index():
    return "View Class quiz_questions"

# Create
@quiz_questions.route('/addQuestion',methods = ['POST'])
def insert():
    try:
        if request.content_type == 'application/json':
            post_data = request.get_json()
            new_quiz_questions = Quiz_Questions(**post_data)
            db.session.add(new_quiz_questions)
            db.session.commit()
            return jsonify("Successfully created a new quiz_question!")
        return jsonify("Oops something went wrong with the JSON script!")
    except Exception:
        return jsonify({
            "Error Message": "An error occurred in adding, please try again"
        }), 404

# Read
@quiz_questions.route('/getAll',methods = ['GET'])
def return_quiz_questions():
    all_quiz_questions = Quiz_Questions.query.all()
    
    data = [i.to_dict() for i in all_quiz_questions]
    return jsonify(data)

@quiz_questions.route('/getQuestion/<id>',methods = ['GET'])
def return_get_quiz_questions_detail(id):
    try:
        [course_id,class_id,quiz_id,quiz_questions_id] = id.split('-')
        data = Quiz_Questions.query.get((course_id,class_id,quiz_id,quiz_questions_id))
        return jsonify(data.to_dict())
    except Exception:
        return jsonify({
            "Error Message": "quiz_questions with that ID doesn't exists!"
        }),404

# Read    
@quiz_questions.route('/getQuestion/<id>/getAllOptions',methods = ['GET'])
def return_get_all_quiz_questions_options(id):
    try:
        [course_id,class_id,quiz_id,quiz_questions_id] = id.split('-')
        data = Quiz_Questions.query.get((course_id,class_id,quiz_id,quiz_questions_id))
        options = data.options.all()
        allClasses = [i.to_dict() for i in options]
        return jsonify(allClasses)
    except Exception:
        return jsonify({
            "Error Message": "Course with that ID doesn't exists!"
        }),404
        
@quiz_questions.route('/getQuestion/<id>/getAnswer',methods = ['GET'])
def return_get_all_quiz_questions_answers(id):
    try:
        [course_id,class_id,quiz_id,quiz_questions_id] = id.split('-')
        data = Quiz_Questions.query.get((course_id,class_id,quiz_id,quiz_questions_id))
        answer = data.options.filter(Quiz_Questions_Options.is_correct_answer==True)
        allClasses = [i.to_dict() for i in answer]
        return jsonify(allClasses)
    except Exception:
        return jsonify({
            "Error Message": "Course with that ID doesn't exists!"
        }),404
        
# Update
@quiz_questions.route('/updateQuestion/<id>',methods=['PUT'])
def update_quiz_questions(id):
    try:
        [course_id,class_id,quiz_id,quiz_questions_id] = id.split('-')
        record = Quiz_Questions.query.get((course_id,class_id,quiz_id,quiz_questions_id))
        
        if request.content_type == 'application/json':
            put_data = request.get_json()
            duration = put_data.get('duration')
            
            setattr(record, "duration", duration)
            db.session.commit()
            return jsonify('Updated quiz_questions!')
        return jsonify("Something is wrong with the JSON script!")
    except Exception:
        return jsonify({
            "message": "Enter Valid JSON request body or a valid id for database"
        }),404
        
# Delete
@quiz_questions.route('/deleteQuestion/<id>', methods=['DELETE'])
def delete_Todo_Item(id):
    try:
        [course_id,class_id,quiz_questions_id] = id.split('-')
        record = Quiz_Questions.query.get((course_id,class_id,quiz_questions_id))
        db.session.delete(record)
        db.session.commit()
        return jsonify('Deleted')
    except Exception:
        return jsonify({
            "message": "quiz_questions not found in database."
        }), 404