import unittest
import sys
sys.path.insert(0, '.')
from application.models import Todo

class TestToDoList(unittest.TestCase):
    """This test case class test the sample Class we have for the Todos class"""
    
    def test_to_dict(self):
        todo1 = Todo(title="Hello", todo_description="Success!")
        
        self.assertEqual(todo1.to_dict(), {
            'id': None,
            'title': 'Hello',
            'todo_description': 'Success!'}
        )
  
  
# Run only if we run python directly from this file, not when importing
if __name__ == "__main__":
    unittest.main()