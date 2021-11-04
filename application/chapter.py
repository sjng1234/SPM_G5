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
    except Exception as e:
        return jsonify({
            "Error Message": "An error has occurred when adding chapter, please try again"
        }), 404


# # Get all chapters from one class in the course -> Shift to Classes
# @chapter.route("/getOne/<id>", methods = ["GET"])
# def get_all_chapters(id):
#     try:
#         [courid, cid] = id.split("-")
#         record = Chapter.query.filter_by(course_id = courid, class_id = cid).all()
#         result = [i.to_dict() for i in record]
#         return jsonify(result)
#     except:
#         return jsonify({
#             "Error Message": "Chapter is not found"
#         }), 400

# UPDATE
@chapter.route("/update/<courid>/<classid>/<chapid>", methods=["PUT"])
def update_class_detail(courid, classid, chapid):
    try:
        record = Chapter.query.filter_by(course_id = courid, class_id = classid, chapter_id = chapid).first()
        if request.content_type == "application/json":
            put_data = request.get_json()
            name = put_data.get("chapter_name")

            setattr(record, "chapter_name", name)
            db.session.commit()
            return jsonify("Successful update of class content!")
        return jsonify("Something is wrong with the JSON script!")
    except Exception:
        return jsonify({
            "message": "Enter Valid JSON request body or a valid id for database"
        }),404

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
        
# Retrieve All Materials under this chapter
@chapter.route("/<id>/getMaterials", methods = ["GET"])
def get_all_materials(id):
    try:
        [course_id, class_id, chapter_id] = id.split("-")
        all_materials = Chapter.query.filter_by(course_id = course_id, class_id = class_id, chapter_id = chapter_id).first().materials.all()
        output = [i.to_dict() for i in all_materials]
        return jsonify(output)
    except Exception as e:
        # print(str(e))
        return jsonify({
            "Error Message": "Invalid Chapter"
        })