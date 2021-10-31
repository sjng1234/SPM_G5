from flask import Blueprint, request, jsonify

from .models import Quiz
from .extensions import db

quiz = Blueprint('quiz', __name__, url_prefix="/quiz")

@quiz.route('/')
def todo_index():
    return "View Class Quizzes"

# Create
@quiz.route('/addQuiz',methods = ['POST'])
def insert():
    try:
        if request.content_type == 'application/json':
            post_data = request.get_json()
            new_quiz = Quiz(**post_data)
            db.session.add(new_quiz)
            db.session.commit()
            return jsonify("Successfully created a new quiz!")
        return jsonify("Oops something went wrong with the JSON script!")
    except Exception:
        return jsonify({
            "Error Message": "An error occurred in adding, please try again"
        }), 404

# Read
@quiz.route('/getAll',methods = ['GET'])
def return_quizzes():
    all_quizzes = Quiz.query.all()
    
    data = [i.to_dict() for i in all_quizzes]
    return jsonify(data)

@quiz.route('/getQuiz/<id>',methods = ['GET'])
def return_get_quiz_detail(id):
    print(id)
    try:
        [course_id,class_id,quiz_id] = id.split('-')
        data = Quiz.query.get((course_id,class_id,quiz_id))
        return jsonify(data.to_dict())
    except Exception:
        return jsonify({
            "Error Message": "Course with that ID doesn't exists!"
        }),404

# Read (Get all classes of a course)   
@quiz.route('/getQuiz/<id>/getAllQn',methods = ['GET'])
def return_get_all_quiz_questions(id):
    try:
        [course_id,class_id,quiz_id] = id.split('-')
        data = Quiz.query.get((course_id,class_id,quiz_id))
        classes = data.questions.all() # Query All Classes for the Specific Course (Syntax: <queried_data>.<relationship>.all())
        allClasses = [i.to_dict() for i in classes]
        return jsonify(allClasses)
    except Exception:
        return jsonify({
            "Error Message": "Course with that ID doesn't exists!"
        }),404
        
# Update
@quiz.route('/updateQuiz/<id>',methods=['PUT'])
def update_quiz(id):
    try:
        [course_id,class_id,quiz_id] = id.split('-')
        record = Quiz.query.get((course_id,class_id,quiz_id))
        print(request.body.content_type)
        if request.Content_Type == 'application/json':
            put_data = request.get_json()
            print(put_data)
            class_id = put_data.get('class_id')
            course_id = put_data.get('course_id')
            question_description = put_data.get('question_description')
            question_id = put_data.get('question_id')
            quiz_id = put_data.get('quiz_id')
            
            setattr(record, "class_id", class_id)
            setattr(record, "course_id", course_id)
            setattr(record, "question_description", question_description)
            setattr(record, "question_id", question_id)
            setattr(record, "quiz_id", quiz_id)
            db.session.commit()
            return jsonify('Updated!')
        return jsonify("Something is wrong with the JSON script!")
    except Exception:
        return jsonify({
            "message": "Enter Valid JSON request body or a valid id for database"
        }),404
        
# Delete
@quiz.route('/deleteCourse/<id>', methods=['DELETE'])
def delete_Todo_Item(id):
    try:
        record = Course.query.get(id)
        db.session.delete(record)
        db.session.commit()
        return jsonify('Deleted')
    except Exception:
        return jsonify({
            "message": "ToDo ID not found in database."
        }), 404