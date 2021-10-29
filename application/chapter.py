from flask import Blueprint, json, request, jsonify

from .models import Chapter
from .extensions import db

chapter = Blueprint('chapter', __name__, url_prefix="/chapter")

@chapter.route("/")
def view_chapter():
    return "Hello, this is where u see all the chapters"

# GETALL
@chapter.route("/getAll", methods = ["GET"])
def get_all():
    record = Chapter.query.all()
    print(record)
    for i in record:
        print(i.creator())
    result = [i.to_dict() for i in record]
    return jsonify(result)

# ADD
@chapter.route("/addChapter", methods = ["POST"])
def add_chapter():
    try:
        if request.content_type == "application/json":
            post_data = request.get_json()
            new_chapter = Chapter(**post_data)
            db.session.add(new_chapter)
            db.session.commit()
            return jsonify("New chapter has been added into the class!")
    except Exception:
        return jsonify({
            "Error Message": "An error has occurred when adding chapter, please try again"
        }), 404


# Get all chapters from one class in the course
@chapter.route("/getOne/<courid>/<cid>", methods = ["GET"])
def get_all_chapters(courid, cid):
    try:
        record = Chapter.query.filter_by(course_id = courid, class_id = cid).all()
        result = [i.to_dict() for i in record]
        return jsonify(result)
    except:
        return jsonify({
            "Error Message": "Chapter is not found"
        })


# DELETE
@chapter.route("/delete/<courid>/<cid>/<chapid>", methods = ["DELETE"])
def delete_chapter(courid, cid, chapid):
    try:
        record = Chapter.query.filter_by(course_id = courid, class_id = cid, chapter_id = chapid).first()
        db.session.delete(record)
        db.session.commit()
        return jsonify("Chapter deleted from Class!")
    except Exception:
        return jsonify({
            "Message": "Chapter not found in Class, delete not successful."
        }), 404