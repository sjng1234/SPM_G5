# import os
# from dotenv import dotenv_values
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.sql.schema import Column

# instantiate the app
app = Flask(__name__)
# app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/SPM_LMS'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                           'pool_recycle': 280}
db = SQLAlchemy(app)
# envConfig = dotenv_values(".env")['TEMP']

# enable CORS
CORS(app)

# Model
class Todo(db.Model):
    __tablename__ = "todos"
    id = Column(db.Integer, primary_key=True)
    title = Column(db.String(20))
    todo_description = Column(db.String(100))

    __mapper_args__ = {
        'polymorphic_identity': 'todoitem'
    }

    def __init__(self, title, todo_description):
        self.title = title
        self.todo_description = todo_description

    def __repr__(self):
        return f"{self.id}"


db.create_all()

# sanity check route
@app.route('/', methods=['GET'])
def Welcome():
    return jsonify('Successful! Linked to Flask APP!')

@app.route('/insertToDo',methods = ['POST'])
def insert():
    if request.content_type == 'application/json':
        post_data = request.get_json()
        title = post_data.get('title')
        desc = post_data.get('todo_description')
        new_to_do = Todo(title,desc)
        db.session.add(new_to_do)
        db.session.commit()
        return jsonify("Successfully posted!")
    return jsonify("Oops something went wrong!")

@app.route('/getAll',methods = ['GET'])
def return_Todos():
    all_books = db.session.query(Todo.id,Todo.title,Todo.todo_description).all()
    data = [dict(i) for i in all_books]
    return jsonify(data)

@app.route('/get/<id>',methods = ['GET'])
def return_Todo_Item(id):
    try:
        book = db.session.query(Todo.id,Todo.title,Todo.todo_description).filter(Todo.id == id).first()
        return jsonify(dict(book))
    except Exception:
        return jsonify({
            "message": "ToDo ID not found in database."
        }), 404

@app.route('/delete/<id>', methods=['DELETE'])
def delete_Todo_Item(id):
    try:
        record = db.session.query(Todo).get(id)
        db.session.delete(record)
        db.session.commit()
        return jsonify('Deleted')
    except Exception:
        return jsonify({
            "message": "ToDo ID not found in database."
        }), 404

@app.route('/update/<id>',methods=['PUT'])
def update_item(id):
    try:
        record = db.session.query(Todo).get(id)
        if request.content_type == 'application/json':
            put_data = request.get_json()
            title = put_data.get('title')
            desc = put_data.get('todo_description')
            if 'id' in put_data:
                print(1)
                record.id = put_data.get('id')
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
if __name__ == '__main__':
    app.run(debug=True)
