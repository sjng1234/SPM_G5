import unittest
import sys
sys.path.insert(0, '..')
from application.models import Todo
from application.models import Course

class TestToDoList(unittest.TestCase):
    """This test case class test the sample Class we have for the Todos class"""
    
    def test_to_dict(self):
        todo1 = Todo(title="Hello", todo_description="Success!")
        
        self.assertEqual(todo1.to_dict(), {
            'id': None,
            'title': 'Hello',
            'todo_description': 'Success!'}
        )
class TestCourseList(unittest.TestCase):

    def test_to_dict(self):
        course = Course(course_id="IS111")

        self.assertEqual(course.to_dict(), {
            "course_id": "IS111",
            "title": None,
            "course_description": None}
        )

  
# Run only if we run python directly from this file, not when importing
if __name__ == "__main__":
    unittest.main()