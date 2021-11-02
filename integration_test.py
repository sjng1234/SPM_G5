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
        
class TestCreateCourse(TestIntegration):
    def test_create_course(self):
        
        course_1 = Course(course_id = "TEST12311", course_name="Test Course With ID", course_description="This should be successful!", course_creator_id=1)
        
        db.session.add(course_1)
        db.session.commit()
        
        # Test Success case
        request_body = {
            "course_id" : "TEST123",
            "course_name": "Test Course Normally",
            "course_description": "This should fail",
            "course_creator_id": 1
        }
        
        response = self.client.post('/course/add', data=json.dumps(request_body), content_type='application/json')
        print(response.json)
        self.assert_200(response)
        self.assertEqual(response.json,"Successfully posted!")
        
        # Test No Course ID
        request_body = {
            "course_id": "",
            "course_name": "Test Course Normally",
            "course_description": "This should fail",
            "course_creator_id": 1
        }
        
        response = self.client.post('/course/add', data=json.dumps(request_body), content_type='application/json')
        print(response.json)
        self.assert_404(response)
        self.assertEqual(response.json,{
            "Error Message": "Course ID is required"
        })
        
        # Test Duplicated Course ID
        request_body = {
            "course_id": "TEST123",
            "course_name": "Test Course Duplicated id",
            "course_description": "This should fail",
            "course_creator_id": 1
        }
        response = self.client.post('/course/add', data=json.dumps(request_body), content_type='application/json')
        print(response.json)
        self.assert_404(response)
        self.assertEqual(response.json,{
            "Error Message": "Course ID exists already!"
        })
# Run only if we run python directly from this file, not when importing
if __name__ == "__main__":
    unittest.main()