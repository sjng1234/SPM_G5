from flask import Blueprint, json, request, jsonify

from .models import Material
from .extensions import db

material = Blueprint('material', __name__, url_prefix="/material")

@material.route('/', methods=['GET'])
def test_material():
    return jsonify("Material Root Route")

@material.route('/add', methods=['PUT'])
def add_material():
    try:
        data = request.get_json()
        material = Material(**data)
        db.session.add(material)
        db.session.commit()
        return jsonify("Successfully Added Material!")
    except Exception as e:
        print(str(e))
        return jsonify({
            "Error Message": "Please ensure that the course,class and chapter id are valid"
        }), 400