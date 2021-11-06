import unittest
import sys
from unittest.case import TestCase
sys.path.insert(0, '.')
from application.models import Badge, Learner_Enrolment, Material_Completion_Status, Qualifications, Quiz_Results, Course, Classes, Chapter, Material, Quiz, Admin, Trainer, User, Quiz_Questions, Quiz_Questions_Options, Learner, Course_Prequisites

# Test Case ID : TU01 (Authored by: Adrian)
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

# Test Case ID : TU02 (Authored by: Ambrose)
class TestClassesList(unittest.TestCase):

    def test_to_dict(self):
        class1 = Classes(course_id="IS111", class_id=1, class_creator_id="Lee Yeow Leong")
        class2 = Classes(course_id="IS110", class_id=1, class_creator_id="Patrick Thng", 
                start_datetime="10/9/2021", class_size=40)
        
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
    
# Test Case ID : TU03 (Authored by: Justin)
class TestChapterList(unittest.TestCase):
    def test_to_dict(self):
        chapter1 = Chapter(course_id="IS111", class_id=1, chapter_id=1, chapter_name="String Methods")
        chapter2 = Chapter(course_id="IS110", class_id=1, chapter_id=2, chapter_name="Fintech Business Case")
    
        self.assertEqual(chapter1.to_dict(), {
            "course_id": "IS111",
            "class_id": 1,
            "chapter_id": 1,
            "chapter_name": "String Methods"
        })

        self.assertEqual(chapter2.to_dict(), {
            "course_id": "IS110",
            "class_id": 1,
            "chapter_id": 2,
            "chapter_name": "Fintech Business Case"
        })
# -------------------------------------
# Test Case ID : TU04 (Authored by: Shen Jie)
class TestMaterialList(unittest.TestCase):
    def test_to_dict(self):
        material1 = Material(course_id="IS111", class_id=1, chapter_id=1, material_name="Material 1", material_id=1)
        material2 = Material(course_id="IS111", class_id=1, chapter_id=2, material_id=1,material_name="Material 2", material_reference="This is the first material for the 2nd chapter")

        self.assertEqual(material1.to_dict(), {
            "course_id": "IS111",
            "class_id": 1,
            "chapter_id": 1,
            "material_id": 1,
            "material_name":"Material 1",
            "material_reference": None
        })

        self.assertEqual(material2.to_dict(), {
            "course_id": "IS111",
            "class_id": 1,
            "chapter_id": 2,
            "material_id": 1,
            "material_name":"Material 2",
            "material_reference": "This is the first material for the 2nd chapter"
        })

# Test Case ID : TU05 (Authored by: Shen Jie)
class TestQuizList(unittest.TestCase):
    def test_to_dict(self):
        quiz1 = Quiz(course_id="IS111", class_id = 1, quiz_id = 1, duration = 10)
        quiz2 = Quiz(course_id="IS111", class_id = 1, quiz_id = 2, duration = 20)

        self.assertEqual(quiz1.to_dict(), {
            "course_id": "IS111",
            "class_id": 1,
            "quiz_id": 1,
            "duration": 10
        })

        self.assertEqual(quiz2.to_dict(), {
            "course_id": "IS111",
            "class_id": 1,
            "quiz_id": 2,
            "duration": 20
        })

# Test Case ID : TU06 (Authored by: Shen Jie)
class TestQuiz_Questions(unittest.TestCase):
    def test_to_dict(self):
        quiz_Questions1 = Quiz_Questions(course_id="IS111", class_id = 1, quiz_id = 1, question_id = 1)
        quiz_Questions2 = Quiz_Questions(course_id="IS111", class_id = 1, quiz_id = 1, question_id = 2, question_description = "Is X correct?")

        self.assertEqual(quiz_Questions1.to_dict(),{
            "course_id": "IS111",
            "class_id": 1,
            "quiz_id": 1,
            "question_id": 1,
            "question_description": None
        })

        self.assertEqual(quiz_Questions2.to_dict(),{
            "course_id": "IS111",
            "class_id": 1,
            "quiz_id": 1,
            "question_id": 2,
            "question_description":"Is X correct?"
        })

# Test Case ID : TU07 (Authored by: Shen Jie)
class TestQuiz_Questions_Options(unittest.TestCase):
    def test_to_dict(self):
        quiz_Questions_Options1 = Quiz_Questions_Options(course_id="IS111", class_id = 1, quiz_id = 1, question_id = 1, option = "Option A", is_correct_answer = True)
        quiz_Questions_Options2 = Quiz_Questions_Options(course_id="IS111", class_id = 1, quiz_id = 1, question_id = 1, option = "Option B", is_correct_answer = False)

        self.assertEqual(quiz_Questions_Options1.to_dict(),{
            "course_id": "IS111",
            "class_id": 1,
            "quiz_id": 1,
            "question_id": 1,
            "option": "Option A",
            "is_correct_answer" : True
        })

        self.assertEqual(quiz_Questions_Options2.to_dict(),{
            "course_id": "IS111",
            "class_id": 1,
            "quiz_id": 1,
            "question_id": 1,
            "option": "Option B",
            "is_correct_answer" : False
        })

# Test Case ID : TU08 (Authored by: Hein)
class TestUser(unittest.TestCase):
    def test_to_dict(self):
        user1 = User(user_id= 1, name= "Adrian", department= "Engineering", user_type="learner")  
        user2 = User(user_id= 2, name= "Ambrose", position= "Sales Manager")

        self.assertEqual(user1.to_dict(),{
            "user_id": 1,
            "name": "Adrian",
            "department": "Engineering",
            "position": None,
            "user_type": "learner",
        })

        self.assertEqual(user2.to_dict(),{
            "user_id": 2,
            "name": "Ambrose",
            "department": None,
            "position": "Sales Manager",
            "user_type": "user",
        })

    # Test Case ID : TU09 (Authored by: Hein)
    def test_get_name(self):
        user3 = User(user_id= 3, name= "Justin", position="General Manager")

        self.assertEqual(user3.get_user_name(), "Justin")

# Test Case ID : TU10 (Authored by: Hein)
class TestLearner(unittest.TestCase):
    def test_to_dict(self):
        learner1 = Learner(user_id = 6, learner_id = 6)
        learner2 = Learner(user_id= 14, learner_id = 8)

        self.assertEqual(learner1.to_dict(), {
            "learner_id": 6,
            "user_id":6,
            "name": None,
            "department": None,
            "position": None,
            "user_type": "learner"
        })

        self.assertEqual(learner2.to_dict(), {
            "learner_id": 8,
            "user_id":14,
            "name": None,
            "department": None,
            "position": None,
            "user_type": "learner"
        })

    # Test Case ID : TU11 (Authored by: Hein)
    def test_get_name(self):
        learner3 = Learner(name = "Adrian", learner_id = 14)

        self.assertEqual(learner3.get_user_name(), "Adrian")

# Test Case ID : TU12 (Authored by: Hein)
class TestTrainer(unittest.TestCase):
    def test_to_dict(self):
        trainer1 = Trainer(user_id = 12, trainer_id = 12)
        
        self.assertEqual(trainer1.to_dict(),{
            "user_id":12,
            "trainer_id":12,
            "name": None,
            "department": None,
            "position": None,
            "user_type": "trainer"
        })
    # Test Case ID : TU13 (Authored by: Hein)
    def test_get_name(self):
        Trainer2 = Learner(name = "Justin", learner_id = 14)

        self.assertEqual(Trainer2.get_user_name(), "Justin")

# Test Case ID : TU14 (Authored by: Hein)
class TestAdmin(unittest.TestCase):
    def test_to_dict(self): #inherited from User
        admin1 = Admin(user_id =1, admin_id=1)
        admin2 = Admin(user_id=41, name="Ambrose", department="Human Resource")
        admin3 = Admin(user_id=42, name="Justin", position="Senior Recruiter")

        self.assertEqual(admin1.to_dict(), {
            "user_id":1,
            "admin_id":1,
            "name": None,
            "department": None,
            "position": None,
            "user_type": 'admin'
        })

        self.assertEqual(admin2.to_dict(),{
            "user_id":41,
            "admin_id": None,
            "name": "Ambrose",
            "department": "Human Resource",
            "position": None,
            "user_type": 'admin'
        })

    # Test Case ID : TU15 (Authored by: Hein)
    def test_get_name(self):
        admin4 = Admin(user_id=42, name="Hein", position="Senior Associate")
        self.assertEqual(admin4.get_user_name(), "Hein")
        
# Test Case ID : TU16 (Authored by: Hein)
class TestQualifications(unittest.TestCase):
    def test_to_dict(self):
        qualification1 = Qualifications(trainer_id=51, course_id="IS111")

        self.assertEqual(qualification1.to_dict(),{
            "trainer_id":51,
            "course_id": "IS111"           
        })

# Test Case ID : TU17 (Authored by: Shen Jie)
class TestLearner_Enrolment(unittest.TestCase):
    def test_to_dict(self):
        learner_enrolment1 = Learner_Enrolment(learner_id=1, course_id="IS111", class_id=1, enrol_date="2021/08/18")
        learner_enrolment2 = Learner_Enrolment(learner_id=1, course_id="IS110", class_id=2)

        self.assertEqual(learner_enrolment1.to_dict(), {
            "learner_id":1,
            "course_id":"IS111",
            "class_id":1,
            "enrol_date": "2021/08/18"
        })

        self.assertEqual(learner_enrolment2.to_dict(), {
            "learner_id":1,
            "course_id":"IS110",
            "class_id":2,
            "enrol_date": None
        })

# Test Case ID : TU18 (Authored by: Hein)
class TestBadge(unittest.TestCase):
    def test_to_dict(self):
        badge1 = Badge(learner_id=1, course_id="IS111", is_qualified=True)

        self.assertEqual(badge1.to_dict(), {
            "learner_id":1,
            "course_id": "IS111",
            "is_qualified":True
        })

# Test Case ID : TU19 (Authored by: Shen Jie)
class TestQuiz_Results(unittest.TestCase):
    def test_to_dict(self):
        quiz_results1 = Quiz_Results(learner_id=1, course_id="IS111", class_id=1, quiz_id=1, score=12)

        self.assertEqual(quiz_results1.to_dict(),{
            "learner_id":1,
            "course_id":"IS111",
            "class_id":1,
            "quiz_id":1,
            "score":12
        })

# Test Case ID : TU20 (Authored by: Justin)
class TestMaterial_Completion_StatusTest(unittest.TestCase):
    def test_to_dict(self):
        material_completion_status1 = Material_Completion_Status(learner_id = 1, course_id = "IS111", class_id = 1, chapter_id = 1, material_id = 1, material_name="Material 1", is_completed = True)

        self.assertEqual(material_completion_status1.to_dict(),{
            "learner_id":1,
            "course_id":"IS111",
            "class_id":1,
            "chapter_id":1,
            "material_id":1,
            "material_name": "Material 1",
            "is_completed":True
        })

# Test Case ID : TU21 (Authored by: Ambrose)
class TestCoursePreReq(unittest.TestCase):
    def test_to_dict(self):
        course_prereq1 = Course_Prequisites(course_id = "IS111", prereq_course_id = "IS110")

        self.assertEqual(course_prereq1.to_dict(),{
            "course_id": "IS111",
            "prereq_course_id": "IS110"
        })
    
# Run only if we run python directly from this file, not when importing
if __name__ == "__main__":
    unittest.main()
