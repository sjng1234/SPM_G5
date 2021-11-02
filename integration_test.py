import unittest
import flask_testing
import json
import sys
sys.path.insert(0, '.')
from application import app
from application.extensions import db
from application.models import *

class TestIntegration(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True

    def create_app(self):
        return app
    
    def setUp(self):
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestCreateTodo(TestIntegration):
    def test_create_todo(self):
        todo1 = Todo(title="Hello", todo_description="Success!")
        db.session.add(todo1)
        db.session.commit()
        
        request_body = {
            "title": "Hello",
            "todo_description": "Success!"
        }
        
        response = self.client.post('/todo/insertToDo', data=json.dumps(request_body), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,'Successfully posted!')
        
        
# Run only if we run python directly from this file, not when importing
if __name__ == "__main__":
    unittest.main()