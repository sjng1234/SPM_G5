import unittest
import sys
sys.path.insert(0, '.')
from application.models import Todo
from application.models import Course
from application.models import Class

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
            "course_name": None,
            "course_description": None,
            "course_creator_id": None,
            "date_created": None}
        )

class TestClassList(unittest.TestCase):

    def test_to_dict(self):
        class1 = Class(course_id="IS111", class_id=1, class_creator_id="Lee Yeow Leong")
        class2 = Class(course_id="IS110", class_id=1, class_creator_id="Patrick Thng", start_datetime="10/9/2021", class_size=40)

        self.assertEqual(class1.to_dict(), {
            "course_id": "IS111",
            "class_id": 1,
            "class_creator_id": "Lee Yeow Leong",
            "start_datetime": None,
            "end_datetime": None,
            "class_size": None,
            "trainer_id": None
        })

        self.assertEqual(class2.to_dict(), {
            "course_id": "IS110",
            "class_id": 1,
            "class_creator_id": "Patrick Thng",
            "start_datetime": "10/9/2021",
            "end_datetime": None,
            "class_size": 40,
            "trainer_id": None
        })
  
# Run only if we run python directly from this file, not when importing
if __name__ == "__main__":
    unittest.main()
