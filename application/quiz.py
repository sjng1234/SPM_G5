from flask import Blueprint, request, jsonify

from .models import Quiz, Quiz_Questions_Options
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

# Get Quiz 
@quiz.route('/getQuiz/<id>',methods = ['GET'])
def return_get_quiz_detail(id):
    try:
        [course_id,class_id,quiz_id] = id.split('-')
        data = Quiz.query.get((course_id,class_id,quiz_id))
        questions = data.questions.all()
        quiz_details = data.to_dict()
        print(quiz_details)
        qn_count = 1
        for question in questions:
            question_details = question.to_dict()
            options = question.options.all()
            option_count = 1
            for option in options:
                option_detail = option.to_dict()
                question_details[f"o{option_count}"] = option_detail
                option_count += 1
            quiz_details[f"q{qn_count}"] = question_details
            qn_count += 1

        return quiz_details
    except Exception:
        return jsonify({
            "Error Message": "Quiz with that ID doesn't exists!"
        }),404

# Get Quiz Answer Sheet
@quiz.route('/getQuizAnswers/<id>',methods = ['GET'])
def return_get_quiz_answers(id):
    try:
        [course_id,class_id,quiz_id] = id.split('-')
        data = Quiz.query.get((course_id,class_id,quiz_id))
        questions = data.questions.all()
        quiz_details = data.to_dict()
        qn_count = 1
        
        for question in questions:
            print(question)
            option = question.options.filter(Quiz_Questions_Options.is_correct_answer==True)
            option_detail = [i.to_dict() for i in option]
            quiz_details[f"q{qn_count}"] = option_detail
            qn_count += 1

        return quiz_details
    except Exception:
        return jsonify({
            "Error Message": "Quiz with that ID doesn't exists!"
        }),404

# Get Quiz Questions Only   
@quiz.route('/getQuiz/<id>/getAllQn',methods = ['GET'])
def return_get_all_quiz_questions(id):
    try:
        [course_id,class_id,quiz_id] = id.split('-')
        data = Quiz.query.get((course_id,class_id,quiz_id))
        questions = data.questions.all()
        allClasses = [i.to_dict() for i in questions]
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
        
        if request.content_type == 'application/json':
            put_data = request.get_json()
            duration = put_data.get('duration')
            
            setattr(record, "duration", duration)
            db.session.commit()
            return jsonify('Updated Quiz!')
        return jsonify("Something is wrong with the JSON script!")
    except Exception:
        return jsonify({
            "message": "Enter Valid JSON request body or a valid id for database"
        }),404
        
# Delete
@quiz.route('/deleteQuiz/<id>', methods=['DELETE'])
def delete_Todo_Item(id):
    try:
        [course_id,class_id,quiz_id] = id.split('-')
        record = Quiz.query.get((course_id,class_id,quiz_id))
        db.session.delete(record)
        db.session.commit()
        return jsonify('Deleted')
    except Exception:
        return jsonify({
            "message": "Quiz not found in database."
        }), 404