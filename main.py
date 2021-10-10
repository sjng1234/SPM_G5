# import os
# from dotenv import dotenv_values
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# configuration
DEBUG = True

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
CORS(app, resources={r'/*': {'origins': '*'}})

# Model
class Todo(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    todo_description = db.Column(db.String(100))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, title, todo_description):
        self.title = title
        self.todo_description = todo_description

    def __repr__(self):
        return f"{self.id}"


db.create_all()


# sanity check route
@app.route('/', methods=['GET'])
def Welcome():
    # print(envConfig)
    return jsonify('Successful! Linked to Flask APP!')


if __name__ == '__main__':
    app.run()
