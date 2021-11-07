import unittest
import flask_testing
import json
import sys
import unittest.mock
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
        
# Test Case ID: TI01 (Authored by: Hein)
class TestCreateUsers(TestIntegration):
    def test_create_users(self):
        # Create Admin, Trainer and Learners
        request_body = {
            "user_id": 1,
            "user_type": "admin",
            "name": "Admin",
            "department": "HR",
            "position": "HR Senior"
        }
        response = self.client.post('/admin/create', data=json.dumps(request_body), content_type='application/json')
        # print(response.json)
        self.assert200(response)
        request_body = {
            "user_id": 2,
            "user_type": "trainer",
            "name": "Trainer",
            "department": "Engineering",
            "position": "Senior Engineer"
        }
        response = self.client.post('/admin/create', data=json.dumps(request_body), content_type='application/json')
        self.assert200(response)
        # print(response.json)
        self.assert200(response)
        request_body = {
            "user_id": 3,
            "user_type": "learner",
            "name": "Learner",
            "department": "Engineering",
            "position": "Junior Engineer"
        }
        response = self.client.post('/admin/create', data=json.dumps(request_body), content_type='application/json')
        self.assert200(response)
        
        # GetAll and check to see if the 3 types of users are successfully created
        response = self.client.get('/admin/getAll')
        # print(response.json)
        self.assert200(response)
        self.assertEqual(response.json,[{'admin_id': 1, 'department': 'HR', 'name': 'Admin', 'position': 'HR Senior', 'user_id': 1, 'user_type': 'admin'}, {'department': 'Engineering', 'name': 'Trainer', 'position': 'Senior Engineer', 'trainer_id': 2, 'user_id': 2, 'user_type': 'trainer'}, {'department': 'Engineering', 'learner_id': 3, 'name': 'Learner', 'position': 'Junior Engineer', 'user_id': 3, 'user_type': 'learner'}])

# Test Case ID: TI02 (Authored by: Adrian)
class TestCreateCourse(TestIntegration):
    def test_create_course(self):
        # Create Users First
        TestCreateUsers.test_create_users(self)
                
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
        # print(response.json)
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
        # print(response.json)
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
        # print(response.json)
        self.assert_404(response)
        self.assertEqual(response.json,{
            "Error Message": "Course ID exists already!"
        })        
# Test Case ID: TI03 (Authored by: Adrian)
class TestGetAllCourse(TestIntegration):
    def test_get_all_course(self):
        # Create Users First
        TestCreateUsers.test_create_users(self)
        
        course_1 = Course(course_id = "TEST12311", course_name="Course 1", course_description="This is course 1", course_creator_id=1)
        course_2 = Course(course_id = "TEST12312", course_name="Course 2", course_description="This is course 2", course_creator_id=1)

        db.session.add(course_1)
        db.session.add(course_2)
        db.session.commit()
        
        response = self.client.get('/course/getAll')
        # print(response.json)
        self.assert_200(response)
        self.assertEqual(response.json,
            [{'course_creator_id': '1', 'course_description': 'This is course 1', 'course_id': 'TEST12311', 'course_name': 'Course 1', 'date_created': None}, {'course_creator_id': '1', 'course_description': 'This is course 2', 'course_id': 'TEST12312', 'course_name': 'Course 2', 'date_created': None}]
        )

# Test Case ID: TI04 (Authored by: Adrian)
class TestGetOneCourse(TestIntegration):
    def test_get_one_course(self):
        # Create Users First
        TestCreateUsers.test_create_users(self)
        
        course_1 = Course(course_id = "TEST12311", course_name="Course 1", course_description="This is course 1", course_creator_id=1)
        course_2 = Course(course_id = "TEST12312", course_name="Course 2", course_description="This is course 2", course_creator_id=1)

        db.session.add(course_1)
        db.session.add(course_2)
        db.session.commit()
        
        response = self.client.get('/course/getCourse/TEST12311')
        # print(response.json)
        self.assert_200(response)
        self.assertEqual(response.json,
            {'course_creator_id': '1', 'course_description': 'This is course 1', 'course_id': 'TEST12311', 'course_name': 'Course 1', 'date_created': None}
        )

# Test Case ID: TI05 (Authored by: Adrian)
class TestUpdateCourse(TestIntegration):
    def test_update_course(self):
        # Create Users First
        TestCreateUsers.test_create_users(self)
        
        course_1 = Course(course_id = "TEST12311", course_name="Course 1", course_description="This is course 1", course_creator_id=1)
        db.session.add(course_1)
        db.session.commit()
        
        # Update the Course Name Update course1
        request_body = {
            "course_name": "Test Update Course",
            "course_description": "This should Pass",
            "course_creator_id": 1
        }
        
        response = self.client.put('/course/update/TEST12311', data=json.dumps(request_body), content_type='application/json')
        
        # print(response.json)
        self.assert200(response)
        self.assertEqual(response.json,'Updated!')
        
        # Check if update has been successful
        response = self.client.get('/course/getCourse/TEST12311')
        self.assert200(response)
        self.assertEqual(response.json,
            {'course_creator_id': '1', 'course_description': 'This should Pass', 'course_id': 'TEST12311', 'course_name': 'Test Update Course', 'date_created': None}
        )
        
        # Trying to update a non-exist course ID
        response = self.client.put('/course/update/TEST12313', data=json.dumps(request_body), content_type='application/json')
        # print(response.json)
        self.assert404(response)
        self.assertEqual(response.json,{
            "message": "Enter Valid JSON request body or a valid id for database"
        })

# Test Case ID: TI06 (Authored by: Adrian)
class TestDeleteCourse(TestIntegration):
    def test_delete_course(self):
        # Create Users First
        TestCreateUsers.test_create_users(self)
        
        course_1 = Course(course_id = "TEST12311", course_name="Course 1", course_description="This is course 1", course_creator_id=1)
        course_2 = Course(course_id = "TEST12312", course_name="Course 2", course_description="This is course 2", course_creator_id=1)

        db.session.add(course_1)
        db.session.add(course_2)
        
        # Trying to delete a non-exist course ID
        response = self.client.delete('/course/delete/TEST12312')
        # print(response)
        self.assert200(response)
        self.assertEqual(response.json,"Deleted")

        # GetAll to check if its really deleted
        response = self.client.get('/course/getAll')
        self.assert200(response)
        self.assertEqual(response.json,
            [{'course_creator_id': '1', 'course_description': 'This is course 1', 'course_id': 'TEST12311', 'course_name': 'Course 1', 'date_created': None}]
        )

        # Trying to delete a non-exist course ID
        response = self.client.delete('/course/delete/TEST12313')
        self.assert404(response)
        self.assertEqual(response.json,{
            "message": "Course ID does not exist in the database"
        })

# Test Case ID: TI07 (Authored by: Ambrose)
class TestCreateClass(TestIntegration):
    def test_create_class(self):
        # Create Users First
        TestCreateUsers.test_create_users(self)
        
        course_1 = Course(course_id = "TEST12311", course_name="Course 1", course_description="This is course 1", course_creator_id=1)
        db.session.add(course_1)
        class_1 = Classes(course_id = "TEST12311",class_id=1, class_creator_id=1, trainer_id=2, class_size=40)
        db.session.add(class_1)
        db.session.commit()
        
        request_body = {
            "course_id": "TEST12311",
            "class_id": 2, #different class of the same course
            "class_creator_id": 1,
            "class_size": 40
        }
        
        response = self.client.post('/classes/add', data=json.dumps(request_body), content_type='application/json')
        # print(response.json)
        self.assert200(response)
        self.assertEqual(response.json,'Successfully created a new class!')

        # # Test Adding Duplicated Class ID
        # request_body = {
        #     "course_id": "TEST12311",
        #     "class_id": 1, #different class of the same course
        #     "class_creator_id": 1,
        #     "class_size": 40
        # }
        
        # response = self.client.post('/classes/add', data=json.dumps(request_body), content_type='application/json')
        # # print(response.json)
        # self.assert404(response)
        # self.assertEqual(response.json,{
        #     "Error Message": "An error has occurred when adding class, please try again"
        # })

# Test Case ID: TI08 (Authored by: Ambrose)
class TestRetrieveAllClassFromAllCourse(TestIntegration):
    def test_retrieve_all_class_from_all_course(self):
        # Create Users first
        TestCreateUsers.test_create_users(self)

        # Create the course and classes
        course_1 = Course(course_id = "TEST12311", course_name="Course 1", course_description="This is course 1", course_creator_id=1)
        course_2 = Course(course_id = "TEST12312", course_name="Course 2", course_description="This is course 2", course_creator_id=1)
        db.session.add(course_1)
        db.session.add(course_2)
        # db.session.commit()
        
        class_1 = Classes(course_id = "TEST12311",class_id=1, class_creator_id=1, trainer_id=2, class_size=40)
        class_2 = Classes(course_id = "TEST12311",class_id=2, class_creator_id=1, trainer_id=2, class_size=40)
        class_3 = Classes(course_id = "TEST12312",class_id=1, class_creator_id=1, trainer_id=2, class_size=40)
        db.session.add(class_1)
        db.session.add(class_2)
        db.session.add(class_3)
        db.session.commit()
        
        response = self.client.get('/classes/getAll')
        # print(response.json)
        self.assert200(response)
        self.maxDiff = None
        self.assertCountEqual(response.json,[
            {
                "class_creator_id": 1,
                "class_id": 1,
                "class_size": 40,
                "course_creator_id": '1',
                "course_description": "This is course 1",
                "course_id": "TEST12311",
                "course_name": "Course 1",
                "date_created": None,
                "department": "Engineering",
                "end_datetime": None,
                "name": "Trainer",
                "position": "Senior Engineer",
                "start_datetime": None,
                "trainer_id": 2,
                "user_id": 2,
                "user_type": "trainer"
            },
            {
                "class_creator_id": 1,
                "class_id": 2,
                "class_size": 40,
                "course_creator_id": '1',
                "course_description": "This is course 1",
                "course_id": "TEST12311",
                "course_name": "Course 1",
                "date_created": None,
                "department": "Engineering",
                "end_datetime": None,
                "name": "Trainer",
                "position": "Senior Engineer",
                "start_datetime": None,
                "trainer_id": 2,
                "user_id": 2,
                "user_type": "trainer"
            },
            {
                "class_creator_id": 1,
                "class_id": 1,
                "class_size": 40,
                "course_creator_id": '1',
                "course_description": "This is course 2",
                "course_id": "TEST12312",
                "course_name": "Course 2",
                "date_created": None,
                "department": "Engineering",
                "end_datetime": None,
                "name": "Trainer",
                "position": "Senior Engineer",
                "start_datetime": None,
                "trainer_id": 2,
                "user_id": 2,
                "user_type": "trainer"
            }
        ])

# Test Case ID: TI09 (Authored by: Ambrose)
class TestRetrieveSpecificClassDetails(TestIntegration):
    def test_retrieve_specific_class_details(self):
        # Create Users first
        TestCreateUsers.test_create_users(self)

        # Create the course and classes
        course_1 = Course(course_id = "TEST12311", course_name="Course 1", course_description="This is course 1", course_creator_id=1)
        db.session.add(course_1)
        
        class_1 = Classes(course_id = "TEST12311",class_id=1, class_creator_id=1, trainer_id=2, class_size=40)
        db.session.add(class_1)
        db.session.commit()
        
        # Testing Getting Specific Class Details
        response = self.client.get('/classes/get/TEST12311-1')
        self.assert200(response)
        self.assertEqual(response.json,{'class_creator_id': 1, 'class_id': 1, 'class_size': 40, 'course_creator_id': '1', 'course_description': 'This is course 1', 'course_id': 'TEST12311', 'course_name': 'Course 1', 'date_created': None, 'department': 'Engineering', 'end_datetime': None, 'name': 'Trainer', 'position': 'Senior Engineer', 'start_datetime': None, 'trainer_id': 2, 'user_id': 2, 'user_type': 'trainer'})
        
# Test Case ID: TI10 (Authored by: Ambrose)
class TestRetrieveAllClassFromOneCourse(TestIntegration):
    def test_retrieve_all_class_from_one_course(self):
        # Create Users First
        TestCreateUsers.test_create_users(self)
        
        # Create the course and classes
        course_1 = Course(course_id = "TEST12311", course_name="Course 1", course_description="This is course 1", course_creator_id=1)
        course_2 = Course(course_id = "TEST12312", course_name="Course 2", course_description="This is course 2", course_creator_id=1)
        db.session.add(course_1)
        db.session.add(course_2)
        # db.session.commit()
        
        class_1 = Classes(course_id = "TEST12311",class_id=1, class_creator_id=1, trainer_id=2, class_size=40)
        class_2 = Classes(course_id = "TEST12311",class_id=2, class_creator_id=1, trainer_id=2, class_size=40)
        class_3 = Classes(course_id = "TEST12312",class_id=1, class_creator_id=1, trainer_id=2, class_size=40)
        db.session.add(class_1)
        db.session.add(class_2)
        db.session.add(class_3)
        db.session.commit()
        
        # Test Getting All Classes from TEST12311
        response = self.client.get('/course/getCourse/TEST12311/getAllClasses')
        self.assert200(response)
        # print(response.json)
        self.assertEqual(response.json,[{'class_creator_id': 1, 'class_id': 1, 'class_size': 40, 'course_id': 'TEST12311', 'end_datetime': None, 'start_datetime': None, 'trainer_id': 2, 'quiz_created': False}, {'class_creator_id': 1, 'class_id': 2, 'class_size': 40, 'course_id': 'TEST12311', 'end_datetime': None, 'start_datetime': None, 'trainer_id': 2, 'quiz_created': False}])

# Test Case ID: TI11 (Authored by: Ambrose)
class TestDeleteClass(TestIntegration):
    def test_delete_class(self):
        # Create Users First
        TestCreateUsers.test_create_users(self)
        
        # Create the course and classes
        course_1 = Course(course_id = "TEST12311", course_name="Course 1", course_description="This is course 1", course_creator_id=1)
        db.session.add(course_1)
        # db.session.commit()
        class_1 = Classes(course_id = "TEST12311",class_id=1, class_creator_id=1, trainer_id=2, class_size=40)
        class_2 = Classes(course_id = "TEST12311",class_id=2, class_creator_id=1, trainer_id=2, class_size=40)
        db.session.add(class_1)
        db.session.add(class_2)
        db.session.commit()
        
        # Test Delete
        response = self.client.delete('/classes/delete/TEST12311-1')
        self.assert200(response)
        self.assertEqual(response.json,"Class deleted from Course!")
        
        # Retrieve Data and See if the Class has been successfully deleted
        response = self.client.get('/classes/getAll')
        self.assert200(response)
        self.assertEqual(response.json,[{'class_creator_id': 1, 'class_id': 2, 'class_size': 40, 'course_creator_id': '1', 'course_description': 'This is course 1', 'course_id': 'TEST12311', 'course_name': 'Course 1', 'date_created': None, 'department': 'Engineering', 'end_datetime': None, 'name': 'Trainer', 'position': 'Senior Engineer', 'start_datetime': None, 'trainer_id': 2, 'user_id': 2, 'user_type': 'trainer'}])

# Test Case ID: TI12 (Authored by: Ambrose)
class TestUpdateClass(TestIntegration):
    def test_update_class(self):        
        # Create Class First
        TestCreateClass.test_create_class(self)
        
        request_body = {
            "class_size": 50
        }
        
        response = self.client.put('/classes/update/TEST12311-1', data=json.dumps(request_body), content_type='application/json')
        self.assert200(response)
        self.assertEqual(response.json,"Successful update of class content!")
        
        # Retrieve Data and See if the Class has been successfully updated
        response = self.client.get('/classes/get/TEST12311-1')
        self.assert200(response)
        self.assertEqual(response.json,{'class_creator_id': 1, 'class_id': 1, 'class_size': 50, 'course_creator_id': '1', 'course_description': 'This is course 1', 'course_id': 'TEST12311', 'course_name': 'Course 1', 'date_created': None, 'department': 'Engineering', 'end_datetime': None, 'name': 'Trainer', 'position': 'Senior Engineer', 'start_datetime': None, 'trainer_id': 2, 'user_id': 2, 'user_type': 'trainer'})

# Test Case ID: TI13 (Authored by: Shen Jie)
class TestCreateQuiz(TestIntegration):
    def test_create_quiz(self):
        # Create Class First
        TestCreateClass.test_create_class(self)
        
        request_body = {
            "course_id": "TEST12311",
            "class_id": 1,
            "duration": 40,
            "quiz_id": 1,
            "questions":[
                {
                    "question_description": "Test Question 1",
                    "question_id": 1,
                    "options":[
                        {
                            "is_correct_answer": False,
                            "option": "Yes"
                        },
                        {
                            "is_correct_answer": True,
                            "option": "No"
                        }
                    ]
                },
                {
                    "question_description": "Test Question 2",
                    "question_id": 2,
                    "options":[
                        {
                            "is_correct_answer": False,
                            "option": "Yes"
                        },
                        {
                            "is_correct_answer": True,
                            "option": "No"
                        }
                    ]
                }
            ]
        }
        
        # Create Quiz
        response = self.client.post('/quiz/addQuiz', data=json.dumps(request_body), content_type='application/json')
        self.assert200(response)
        self.assertEqual(response.json,"Successfully created a new quiz! TEST12311-1-1")
        
        # # Test Create Duplicated Quiz
        # response = self.client.post('/quiz/addQuiz', data=json.dumps(request_body), content_type='application/json')
        # self.assert404(response)
        # self.assertEqual(response.json,{
        #     "Error Message": "Quiz ID for this class already exists!"
        # })
        
# Test Case ID: TI14 (Authored by: Shen Jie)
class RetriveClassQuiz(TestIntegration):
    def test_retrive_class_quiz(self):        
        # Create Quiz First
        TestCreateQuiz.test_create_quiz(self)
        
        # Test Retrieve Class Quiz from the class route
        response = self.client.get('/classes/getQuiz/TEST12311-1-1')
        self.assert200(response)
        # # print(response.json)
        self.assertEqual(response.json,{'class_id': 1, 'course_id': 'TEST12311', 'duration': 40, 'question': [{'options': [{'option': 'No'}, {'option': 'Yes'}], 'question_description': 'Test Question 1', 'question_id': 1}, {'options': [{'option': 'No'}, {'option': 'Yes'}], 'question_description': 'Test Question 2', 'question_id': 2}], 'quiz_id': 1})
        
        # Test Retrieve Class Quiz that is non existent
        response = self.client.get('/classes/getQuiz/TEST12311-1-2')
        self.assert400(response)
        self.assertEqual(response.json,{'message': "Quiz ID is invalid"})
        
# Test Case ID: TI15 (Authored by: Shen Jie)
class TestGetQuizAnswers(TestIntegration):
    def test_get_quiz_answers(self):
        # Create Quiz First 
        TestCreateQuiz.test_create_quiz(self)
        
        # Test Get Quiz Answers
        response = self.client.get('/quiz/getQuizAnswers/TEST12311-1-1')
        self.assert200(response)
        # print(response.json)
        self.assertEqual(response.json,{'class_id': 1, 'course_id': 'TEST12311', 'duration': 40, 'answers':{'q1': 'No', 'q2': 'No'}, 'quiz_id': 1})
        
# Test Case ID: TI16 (Authored by: Shen Jie)
class LearnerEnrolInClass(TestIntegration):
    def test_learner_enrol_in_class(self):
        # Create Class and Learner (created in the TC)
        TestCreateClass.test_create_class(self)
        
        # Test Learner (id 3) Enrol in Class (TEST12311-1)
        request_body = {
            "learner_id": 3,
            "course_id": "TEST12311",
            "class_id": 1,
            "enrol_date": None
        }
        response = self.client.post('/learner/enrol', data=json.dumps(request_body), content_type='application/json')
        self.assert200(response)
        self.assertEqual(response.json,"Successfully Enrolled!")
        
# Test Case ID: TI17 (Authored by: Shen Jie)
class TestGetLearnerClassesEnrolled(TestIntegration):
    def test_get_learner_enrolment(self):
        # Run the LearnerEnrolInClass TC first
        LearnerEnrolInClass.test_learner_enrol_in_class(self)
        
        # Test Get Learner Enrolment (id 3)
        response = self.client.get('/learner/getEnrolledClasses/3')
        self.assert200(response)
        
        # Preprocessing the response to remove the enrol_date
        data = response.json
        del data[0]['enrol_date']
        
        self.assertEqual(data,[{'class_id': 1, 'course_id': 'TEST12311', 'learner_id': 3}])
        
# Test Case ID: TI18 (Authored by: Shen Jie)
class TestLearnerDropClass(TestIntegration):
    def test_learner_drop_class(self):
        # Run the LearnerEnrolInClass TC first
        LearnerEnrolInClass.test_learner_enrol_in_class(self)
        
        # Test Learner Drop Class (id 3)
        response = self.client.delete('/learner/drop/TEST12311-1-3')
        self.assert200(response)
        self.assertEqual(response.json,"Successfully Dropped!")
        
        # Test Get Learner Enrolment (id 3)
        response = self.client.get('/learner/getEnrolledClasses/3')
        self.assert200(response)
        self.assertEqual(response.json,[])

# Test Case ID: TI19 (Authored by: Shen Jie)
class TestLearnerUpdateQuizResults(TestIntegration):
    def test_learner_update_results(self):
        # Run the CreateQuiz TC first, learner will be auto created
        TestCreateQuiz.test_create_quiz(self)
        
        request_body = {
            "learner_id": 3,
            "course_id": "TEST12311",
            "class_id": 1,
            "quiz_id": 1,
            "score": 2
        }
        
        # Test Learner Update Quiz Results
        response = self.client.put('/learner/submitQuizResults', data=json.dumps(request_body), content_type='application/json')
        self.assert200(response)
        # print(response.json)
        self.assertEqual(response.json,{'Message': 'Quiz Results Submitted'})
        
# Test Case ID: TI20 (Authored by: Shen Jie)
class TestGetLearnerQuizResults(TestIntegration):
    def test_get_learner_quiz_results(self):
        # Run the LearnerUpdateQuizResults TC first
        TestLearnerUpdateQuizResults.test_learner_update_results(self)
        
        # Test Get Learner Quiz Results
        response = self.client.get('/learner/getAllQuizResults/3')
        self.assert200(response)
        # print(response.json)
        self.assertEqual(response.json,[{'learner_id': 3, 'course_id': 'TEST12311', 'class_id': 1, 'quiz_id': 1, 'score': 2}])

# Test Case ID: TI21 (Authored by: Hein)
class TestUpdateQualifiedTrainer(TestIntegration):
    def test_update_qualified_instructor(self):
        # Create Class and Trainer (created in the TC)
        TestCreateClass.test_create_class(self)
        
        # Update Qualified Trainer (id 2) to class (TEST12311)
        put_data = {
            "course_id": "TEST12311",
            "trainer_id": 2,
        }
        
        response = self.client.put('/trainer/updateQualifications', data=json.dumps(put_data), content_type='application/json')
        self.assert200(response)
        self.assertEqual(response.json,{'Message': "Qualification added successfully"})
        
# Test Case ID: TI22 (Authored by: Hein)
class TestGetQualifiedTrainer(TestIntegration):
    def test_get_qualified_instructor(self):
        # Run the Update Qualified Trainer TC 
        TestUpdateQualifiedTrainer.test_update_qualified_instructor(self)
        
        # Test Get Qualified Trainer for course (TEST12311)
        response = self.client.get('/admin/TEST12311/getAllQualifiedTrainer')
        self.assert200(response)
        self.assertEqual(response.json,[{'trainer_id': 2, 'course_id': 'TEST12311'}])
        
# Test Case ID: TI23 (Authored by: Hein)
class TestGetTrainerListOfQualification(TestIntegration):
    def test_get_trainer_list_of_qualification(self):
        # Run the Update Qualified Trainer TC 
        TestUpdateQualifiedTrainer.test_update_qualified_instructor(self)
        
        # Test Get Trainer List of Qualification (id 2)
        response = self.client.get('/trainer/getAllQualifications/2')
        # print(response.json)
        self.assert200(response)
        self.assertEqual(response.json,['TEST12311'])
        
# Test Case ID: TI24 (Authored by: Hein)
class TestGetTrainerListOfClass(TestIntegration):
    def test_get_trainer_list_of_class(self):
        # Create Class and Trainer (created in the TC)
        TestCreateClass.test_create_class(self)
        
        # Test Get Trainer List of Class (id 2)
        response = self.client.get('/trainer/getAllClasses/2')
        print(response.json)
        self.assert200(response)
        self.assertEqual(response.json,[{'class_creator_id': 1, 'class_id': 1, 'class_size': 40, 'course_id': 'TEST12311', 'end_datetime': None, 'start_datetime': None, 'trainer_id': 2}])

# Test Case ID: TI25 (Authored by: Justin)
class TestCreateChapter(TestIntegration):
    def test_create_chapter(self):
        # Create Class and Trainer (created in the TC)
        TestCreateClass.test_create_class(self)
        
        # Create Chapter (id 1) to class (TEST12311-1)
        request_body = {
            "course_id": "TEST12311",
            "class_id": 1,
            "chapter_id": 1,
            "chapter_name": "Chapter 1",
        }
        
        response = self.client.post('/chapter/addChapter', data=json.dumps(request_body), content_type='application/json')
        self.assert200(response)
        self.assertEqual(response.json,"New chapter has been added into the class!")
        
# Test Case ID: TI26 (Authored by: Justin)
class TestRetrieveClassChapters(TestIntegration):
    def test_retrieve_all_class_chapters(self):        
        # Run Test Class for TestCreateChapter
        TestCreateChapter.test_create_chapter(self)
        
        # Test Retrieve All Class Chapters from class (TEST12311-1)
        response = self.client.get('/classes/getChapters/TEST12311-1')
        self.assert200(response)
        self.assertEqual(response.json,[{'chapter_id': 1, 'chapter_name': 'Chapter 1', 'class_id': 1, 'course_id': 'TEST12311','materials': []}])
        
# Test Case ID: TI27 (Authored by: Justin)
class TestCreateMaterial(TestIntegration):
    def test_create_material(self):
        # Run Test Class for TestCreateChapter
        TestCreateChapter.test_create_chapter(self)
        # Create Material (id 1) for chapter (TEST12311-1-1)
        request_body = {
            "course_id": "TEST12311",
            "class_id": 1,
            "chapter_id": 1,
            "material_id": 1,
            "material_name": "Material 1",
            "material_reference": "https://www.example.com"
        }
        response = self.client.put('/material/add', data=json.dumps(request_body), content_type='application/json')
        self.assert200(response)
        self.assertEqual(response.json,"Successfully Added Material!")
        
# Test Case ID: TI28 (Authored by: Justin)
class TestRetrieveChapterMaterials(TestIntegration):
    def test_retrieve_all_chapter_materials(self):
        # Run Test Class for TestCreateMaterial
        TestCreateMaterial.test_create_material(self)
        
        # Test Retrieve All Class Materials from chapter (TEST12311-1-1)
        response = self.client.get('/chapter/TEST12311-1-1/getMaterials')
        self.assert200(response)
        self.assertEqual(response.json,[{'chapter_id': 1, 'class_id': 1, 'course_id': 'TEST12311', 'material_id': 1, 'material_name': 'Material 1', 'material_reference': 'https://www.example.com'}])

# Test Case ID: TI29 (Authored by: Justin)
class TestLearnerCompleteMaterial(TestIntegration):
    def test_learner_complete_material(self):
        # Run Test Class for TestCreateMaterial (learner_id = 3) should have been created also
        TestCreateMaterial.test_create_material(self)
        
        # Test Learner Complete Material (id 1) for chapter (TEST12311-1-1)
        request_body = {
            "learner_id": 3,
            "course_id": "TEST12311",
            "class_id": 1,
            "chapter_id": 1,
            "material_id": 1,
            "material_name": "Material 1",
            "is_completed": True
        }
        response = self.client.put('/learner/completeMaterial', data=json.dumps(request_body), content_type='application/json')
        self.assert200(response)
        self.assertEqual(response.json,"Successfully Updated Material Completion Status!")

# Test Case ID: TI30 (Authored by: Justin)
class TestRetrieveLearnerCompletedMaterialsOfSpecificClass(TestIntegration):
    def test_retrieve_learner_completed_materials_for_Class(self):
        # Run Test Class for TestLearnerCompleteMaterial
        TestLearnerCompleteMaterial.test_learner_complete_material(self)
        
        # Test Retrieve All Learner Completed Materials
        response = self.client.get('/learner/getCompletedMaterials/TEST12311-1-3')
        self.assert200(response)
        self.assertEqual(response.json,[{'chapter_id': 1, 'class_id': 1, 'course_id': 'TEST12311', 'is_completed': True, 'learner_id': 3, 'material_id': 1, 'material_name': 'Material 1'}])

# Test Case ID: TI31 (Authored by: Ambrose)
class TestAddCoursePreReq(TestIntegration):
    def test_add_course_pre_req(self):
        # Run Test Class for TestGetAllCourse -which will create 2 courses in the process
        TestGetAllCourse.test_get_all_course(self)
        
        # Test Add Prequisites for course (TEST12312), making the course (TEST12311) a prerequisite for course (TEST12312)
        
        request_body = {
            "course_id": "TEST12312",
            "prereq_course_id": "TEST12311"
        }
        
        response = self.client.put('/course/addPreReq', data=json.dumps(request_body), content_type='application/json')
        self.assert200(response)
        self.assertEqual(response.json,"Successfully Added Course Pre-requisite!")

# Test Case ID: TI32 (Authored by: Ambrose)
class TestRetrieveCoursePreReq(TestIntegration):
    def test_retrieve_course_pre_req(self):
        # Run Test Class for TestAddCoursePreReq
        TestAddCoursePreReq.test_add_course_pre_req(self)
        
        # Test Retrieve Course Pre-requisite for course (TEST12312)
        response = self.client.get('/course/TEST12312/getPreReq')
        self.assert200(response)
        print(response.json)
        self.assertEqual(response.json,{'Number_of_Pre-Requisites': 1, 'Pre-Requisites-List': ['TEST12311'], 'course_id': 'TEST12312'})
        
        # Test Retrieve Course Pre-requisite for course (TEST12311)
        response = self.client.get('/course/TEST12311/getPreReq')
        self.assert200(response)
        print(response.json)
        self.assertEqual(response.json,{'Number_of_Pre-Requisites': 0, 'Pre-Requisites-List': [], 'course_id': 'TEST12311'})
        
# Test Case ID: TI33 (Authored by: Hein)
class TestLearnerCompleteCourse(TestIntegration):
    def test_learner_add_badge(self):
        # Run Test Class for getallcourse,classes and learners will be created
        TestGetAllCourse.test_get_all_course(self)
        
        # Test Learner Complete Course (TEST12311)
        request_body = {
            "learner_id": 3,
            "course_id": "TEST12311",
            "is_qualified": True
        }
        response = self.client.post('/learner/addBadge', data=json.dumps(request_body), content_type='application/json')
        self.assert200(response)
        self.assertEqual(response.json,"Successfully Added Course Complete Badge!")

# Test Case ID: TI34 (Authored by: Hein)
class TestRetrieveLearnerBadges(TestIntegration):
    def test_retrieve_learner_badges(self):
        # Run Test Class for TestLearnerCompleteCourse
        TestLearnerCompleteCourse.test_learner_add_badge(self)
        
        # Test Retrieve Learner Badges (learner_id = 3)
        response = self.client.get('/learner/3/getAllBadges')
        self.assert200(response)
        self.assertEqual(response.json,{'badges': ['TEST12311'], 'learner_id': '3', 'num_badges': 1})
        
# Test Case ID: TI35 (Authored by: Shen Jie)
class TestRetrieveAllLearnerDetails(TestIntegration):
    def test_retrieve_all_learner_details(self):
        # Run Test Class for TestCreateUsers
        TestCreateUsers.test_create_users(self)
        
        # Test Retrieve All Learner Details
        response = self.client.get('/admin/getAllLearners')
        self.assert200(response)
        self.assertEqual(response.json,[{'department': 'Engineering', 'learner_id': 3, 'name': 'Learner', 'position': 'Junior Engineer', 'user_id': 3, 'user_type': 'learner'}])
        
# Test Case ID: TI36 (Authored by: Shen Jie)
class TestRetrieveAllTrainerDetails(TestIntegration):
    def test_retrieve_all_trainer_details(self):
        # Run Test Class for TestCreateUsers
        TestCreateUsers.test_create_users(self)
        
        # Test Retrieve All Trainer Details
        response = self.client.get('/admin/getAllTrainers')
        self.assert200(response)
        self.assertEqual(response.json,[{'department': 'Engineering', 'trainer_id': 2, 'name': 'Trainer', 'position': 'Senior Engineer', 'user_id': 2, 'user_type': 'trainer'}])
        
# Test Case ID: TI37 (Authored by: Shen Jie)
class TestRetrieveIndividualDetails(TestIntegration):
    def test_retrieve_individual_details(self):
        # Run Test Class for TestCreateUsers
        TestCreateUsers.test_create_users(self)
        
        # Test Retrieve Individual Details for admin(id1)
        response = self.client.get('/admin/1')
        self.assert200(response)
        self.assertEqual(response.json,{'admin_id': 1, 'department': 'HR', 'name': 'Admin', 'position': 'HR Senior', 'user_id': 1, 'user_type': 'admin'})
        
        # Test Retrieve Individual Details for trainer(id2)
        response = self.client.get('/trainer/2')
        self.assert200(response)
        self.assertEqual(response.json,{'department': 'Engineering', 'name': 'Trainer', 'position': 'Senior Engineer', 'trainer_id': 2, 'user_id': 2, 'user_type': 'trainer'})
        
        # Test Retrieve Individual Details for learners(id3)
        response = self.client.get('/learner/3')
        self.assert200(response)
        self.assertEqual(response.json,{'department': 'Engineering', 'learner_id': 3, 'name': 'Learner', 'position': 'Junior Engineer', 'user_id': 3, 'user_type': 'learner'})
        
        # Getting Invalid User Details for admin/trainer/learner should all be 400
        response = self.client.get('/admin/4')
        self.assert400(response)
        response = self.client.get('/trainer/4')
        self.assert400(response)
        response = self.client.get('/learner/4')
        self.assert400(response)
        
        # Trying to query user details for wrong user type should also be be 400
        response = self.client.get('/admin/2')
        self.assert400(response)
        response = self.client.get('/learner/1')
        self.assert400(response)
        response = self.client.get('/trainer/1')
        self.assert400(response)
        
# Run only if we run python directly from this file, not wh›en importing
if __name__ == "__main__":
    unittest.main()