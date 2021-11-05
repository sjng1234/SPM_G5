from flask import Blueprint, request, jsonify

from .models import Quiz, Quiz_Questions_Options, Quiz_Questions
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
            new_quiz = Quiz(**{
                "course_id" : post_data["course_id"],
                "class_id" : post_data["class_id"],
                "duration" : post_data["duration"],
                "quiz_id" : post_data["quiz_id"]
            })
            db.session.add(new_quiz)
            db.session.commit()
            db.session.flush()
            # print(new_quiz.quiz_id)
            questions = post_data['questions']
            for q in questions:
                question_id = q['question_id']
                question_description = q['question_description']
                new_qn = Quiz_Questions(**{
                    "course_id" : new_quiz.course_id,
                    "quiz_id" : new_quiz.quiz_id,
                    "class_id" : new_quiz.class_id,
                    "question_id" : question_id,
                    "question_description" : question_description
                })
                db.session.add(new_qn)
                db.session.commit()
                db.session.flush()
                # print(new_qn.question_id)
                for o in q["options"]:
                    new_option = Quiz_Questions_Options(**{
                        "course_id" : new_qn.course_id,
                        "quiz_id" : new_qn.quiz_id,
                        "class_id" : new_qn.class_id,
                        "question_id" : new_qn.question_id,
                        "option" : o["option"],
                        "is_correct_answer" : o["is_correct_answer"]
                    })
                    db.session.add(new_option)
                    db.session.commit()
                    db.session.flush()
                    # print(new_option.option)
            return jsonify(f"Successfully created a new quiz! {new_quiz.course_id}-{new_quiz.class_id}-{new_quiz.quiz_id}")
        return jsonify("Oops something went wrong with the JSON script!")
    except Exception as e:
        return jsonify({
            "Error Message": "Quiz ID for this class already exists!"
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
        quiz_details["answers"] = {}
        for question in questions:
            print(question)
            option = question.options.filter(Quiz_Questions_Options.is_correct_answer==True)
            option_detail = [i.to_dict()['option'] for i in option]
            quiz_details["answers"][f"q{qn_count}"] = option_detail[0]
            qn_count += 1

        return quiz_details
    except Exception:
        return jsonify({
            "Error Message": "Quiz with that ID doesn't exists!"
        }),404

# # Get Quiz Questions Only   -> Shifted to classes route
# @quiz.route('/getQuiz/<id>/getAllQn',methods = ['GET'])
# def return_get_all_quiz_questions(id):
#     try:
#         [course_id,class_id,quiz_id] = id.split('-')
#         data = Quiz.query.get((course_id,class_id,quiz_id))
#         questions = data.questions.all()
#         allClasses = [i.to_dict() for i in questions]
#         return jsonify(allClasses)
#     except Exception:
#         return jsonify({
#             "Error Message": "Course with that ID doesn't exists!"
#         }),404

# Update (Not in use yet)
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