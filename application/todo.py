from flask import Blueprint, request, jsonify
# import pymysql

from .models import Todo
from .extensions import db

todo = Blueprint('todo', __name__, url_prefix="/todo")

@todo.route('/')
def todo_index():
    return "Todo Hello"

@todo.route('/insertToDo',methods = ['POST'])
def insert():
    if request.content_type == 'application/json':
        post_data = request.get_json()
        new_to_do = Todo(**post_data)
        db.session.add(new_to_do)
        db.session.commit()
        return jsonify("Successfully posted!")
    return jsonify("Oops something went wrong!")

@todo.route('/getAll',methods = ['GET'])
def return_Todos():
    # db.create_all()
    all_books = Todo.query.all()
    data = [i.to_dict() for i in all_books]
    return jsonify(data)

@todo.route('/get/<id>',methods = ['GET'])
def return_Todo_Item(id):
    # db.create_all()
    try:
        book = Todo.query.get(id)
        return jsonify(book.to_dict())
    except Exception:
        return jsonify({
            "message": "ToDo ID not found in database."
        }), 404

@todo.route('/delete/<id>', methods=['DELETE'])
def delete_Todo_Item(id):
    try:
        record = Todo.query.get(id)
        db.session.delete(record)
        db.session.commit()
        return jsonify('Deleted')
    except Exception:
        return jsonify({
            "message": "ToDo ID not found in database."
        }), 404

@todo.route('/update/<id>',methods=['PUT'])
def update_item(id):
    try:
        record = Todo.query.get(id)
        print(record)
        if request.content_type == 'application/json':
            put_data = request.get_json()
            print(put_data)
            title = put_data.get('title')
            desc = put_data.get('todo_description')
            print(title, desc)
            if 'id' in put_data:
                print(1)
                record.id = id
            record.title = title
            record.todo_description = desc
            db.session.commit()
            return jsonify('Updated!')
        else:
            raise Exception
    except Exception:
        return jsonify({
            "message": "Enter Valid JSON request body or a valid id for database"
        }),404