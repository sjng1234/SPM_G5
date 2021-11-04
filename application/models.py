from .extensions import db
from sqlalchemy.sql.schema import Column, ForeignKey, ForeignKeyConstraint

# Model
# example
class Todo(db.Model):
    __tablename__ = "TODOS"
    id = Column(db.Integer, primary_key=True)
    title = Column(db.String(20))
    todo_description = Column(db.String(100))

    __mapper_args__ = {
        'polymorphic_identity': 'todo'
    }

    def __repr__(self):
        return f"{self.id}"

    def to_dict(self):
        col = self.__mapper__.column_attrs.keys()
        result = {}
        for i in col:
            result[i] = getattr(self, i)
        return result

# Course
class Course(db.Model):
    __tablename__ = "course"
    course_id = Column(db.String(50), primary_key=True)
    course_name = Column(db.String(255))
    course_description = Column(db.String(255))
    course_creator_id = Column(db.String(255), ForeignKey('admin.admin_id'))
    date_created =  Column(db.DateTime)
    classes = db.relationship('Classes', backref="course", lazy="dynamic") # Establish one-to-many relationship between course and classes
    
    __mapper_args__ = {
        'polymorphic_identity': 'course'
    }

    # def __repr__(self):
    #     return f"{self.course_id}"

    def to_dict(self):
        col = self.__mapper__.column_attrs.keys()
        result = {}
        for i in col:
            result[i] = getattr(self, i)
        return result

    def get_course_name(self):
        return getattr(self, "course_name")

# Classes
class Classes(db.Model):
    __tablename__ = "classes"
    course_id = Column(db.String(50), db.ForeignKey("course.course_id"), primary_key = True)
    class_id = Column(db.Integer, primary_key=True)
    class_creator_id = Column(db.Integer)
    start_datetime = Column(db.DateTime)
    end_datetime = Column(db.DateTime)
    class_size = Column(db.Integer)
    trainer_id = Column(db.Integer)
    chapters = db.relationship('Chapter', backref="class", lazy="dynamic") # Establish one-to-many relationship between classes and chapter
    quiz= db.relationship('Quiz', backref="quiz", lazy="dynamic") 

    __mapper_args__ = {
        'polymorphic_identity': 'classes'
    }

    def to_dict(self):
        col = self.__mapper__.column_attrs.keys()
        result = {}
        for i in col:
            result[i] = getattr(self, i)
        return result

# Chapter
class Chapter(db.Model):
    __tablename__ = "chapter"
    course_id = Column(db.String(50), primary_key=True)
    class_id = Column(db.Integer, primary_key=True)
    chapter_id = Column(db.Integer, primary_key=True)
    chapter_name = Column(db.String(255))
    materials = db.relationship("Material", backref="chapter", lazy="dynamic")

    __table_args__ = (
        ForeignKeyConstraint(
            ["class_id", "course_id"],
            ["classes.class_id", "classes.course_id"]
        ), {}
    )

    def to_dict(self):
        col = self.__mapper__.column_attrs.keys()
        result = {}
        for i in col:
            result[i] = getattr(self, i)
        return result
        
# Material
class Material(db.Model):
    __tablename__ = "material"
    course_id = Column(db.String(50), primary_key=True)
    class_id = Column(db.Integer, primary_key=True)
    chapter_id = Column(db.Integer, primary_key=True)
    material_id = Column(db.Integer, primary_key=True)
    material_reference = Column(db.String(255))


    __mapper_args__ = {
        'polymorphic_identity': 'material'
    }

    __table_args__ = (
        ForeignKeyConstraint(
            ["class_id", "course_id", "chapter_id"],
            ["chapter.class_id", "chapter.course_id", "chapter.chapter_id"]
        ), {}
    )

    def to_dict(self):
        col = self.__mapper__.column_attrs.keys()
        result = {}
        for i in col:
            result[i] = getattr(self, i)
        return result

# Quiz
class Quiz(db.Model):
    __tablename__ = "quiz"
    course_id = Column(db.String(50), primary_key = True)
    class_id = Column(db.Integer, primary_key=True)
    quiz_id = Column(db.Integer, primary_key=True)
    duration = Column(db.Integer)
    questions = db.relationship('Quiz_Questions', backref="questions", lazy="dynamic")
    
    __table_args__ = (
        ForeignKeyConstraint(
            ["class_id", "course_id"],
            ["classes.class_id", "classes.course_id"]
        ), {}
    )

    __mapper_args__ = {
        'polymorphic_identity': 'quiz'
    }
    
    def to_dict(self):
        col = self.__mapper__.column_attrs.keys()
        result = {}
        for i in col:
            result[i] = getattr(self, i)
        return result

class Quiz_Questions(db.Model):
    __tablename__ = "quiz_questions"
    course_id = Column(db.String(50), primary_key = True)
    class_id = Column(db.Integer, primary_key=True)
    quiz_id = Column(db.Integer, primary_key=True)
    question_id = Column(db.Integer, primary_key=True)
    question_description = Column(db.String(255), nullable=False)
    options = db.relationship("Quiz_Questions_Options", backref="options",lazy="dynamic")
    
    __mapper_args__ = {
        'polymorphic_identity': 'quiz_questions'
    }

    __table_args__ = (
        ForeignKeyConstraint(
            ["class_id", "course_id", "quiz_id"] ,
            ["quiz.class_id", "quiz.course_id", "quiz.quiz_id"]
        ),
    )

    def to_dict(self):
        col = self.__mapper__.column_attrs.keys()
        result = {}
        for i in col:
            result[i] = getattr(self, i)
        return result

    
class Quiz_Questions_Options(db.Model):
    __tablename__ = "quiz_questions_options"
    course_id = Column(db.String(50), primary_key = True)
    class_id = Column(db.Integer, primary_key=True)
    quiz_id = Column(db.Integer, primary_key=True)
    question_id = Column(db.Integer, primary_key=True)
    option = Column(db.String(255), primary_key=True)
    is_correct_answer = Column(db.Boolean)
    
    __mapper_args__ = {
        'polymorphic_identity': 'quiz_questions_options'
    }

    __table_args__ = (
        ForeignKeyConstraint(
            ["class_id", "course_id", "quiz_id", "question_id"],
            ["quiz_questions.class_id", "quiz_questions.course_id", "quiz_questions.quiz_id", "quiz_questions.question_id"]
        ), {}
    )

    def to_dict(self):
        col = self.__mapper__.column_attrs.keys()
        result = {}
        for i in col:
            result[i] = getattr(self, i)
        return result
    
# User Classes
class User(db.Model):
    __tablename__ = "user"
    user_id = Column(db.Integer, primary_key=True)
    name = Column(db.String(255))
    department = Column(db.String(255))
    position = Column(db.String(255))
    user_type = Column(db.String(255))
    
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': user_type
    }
    
    def to_dict(self):
        col = self.__mapper__.column_attrs.keys()
        result = {}
        for i in col:
            result[i] = getattr(self, i)
        return result

    def get_user_name(self):
        return getattr(self, "name")
    
class Learner(User):
    __tablename__ = "learner"
    learner_id = Column(db.Integer, db.ForeignKey("user.user_id"), primary_key=True)
    classes = db.relationship('Learner_Enrolment', backref="learner_enrolment", lazy="dynamic") # Establish one-to-many relationship between learner and learner_enrolment
    quiz_results = db.relationship('Quiz_Results', backref="quiz_results", lazy="dynamic") # Establish one-to-many relationship between learner and quiz_results

    __mapper_args__ = {
        'polymorphic_identity': 'learner'
    }
    
class Trainer(User):
    __tablename__ = "trainer"
    trainer_id = Column(db.Integer, db.ForeignKey("user.user_id"), primary_key=True)
    all_qualified_course = db.relationship('Qualifications', backref="qualifications", lazy="dynamic") # Establish one-to-many relationship between trainer and Qualifications
    
    __mapper_args__ = {
        'polymorphic_identity': 'trainer' 
    }
    
class Admin(User):
    __tablename__ = "admin"
    admin_id = Column(db.Integer, db.ForeignKey("user.user_id"), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }
    
# qualifications -for trainers
class Qualifications(db.Model):
    __tablename__ = "qualifications"
    trainer_id = Column(db.Integer, db.ForeignKey("trainer.trainer_id"), primary_key=True)
    course_id = Column(db.String(255), db.ForeignKey("course.course_id"),primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'qualifications'
    }
    
    def to_dict(self):
        col = self.__mapper__.column_attrs.keys()
        result = {}
        for i in col:
            result[i] = getattr(self, i)
        return result

# learner_enrolment - for learners (tag to class)
class Learner_Enrolment(db.Model):
    __tablename__ = "learner_enrolment"
    learner_id = Column(db.Integer, db.ForeignKey('learner.learner_id'),primary_key=True)
    course_id = Column(db.String(255), db.ForeignKey('classes.course_id'), primary_key=True)
    class_id = Column(db.Integer, db.ForeignKey('classes.class_id'),primary_key=True)
    enrol_date = Column(db.DateTime)
    
    __mapper_args__ = {
        'polymorphic_identity': 'learner_enrolment'
    }
    
    def to_dict(self):
        col = self.__mapper__.column_attrs.keys()
        result = {}
        for i in col:
            result[i] = getattr(self, i)
        return result

# badges - for learners (tag to course)
class Badge(db.Model):
    __tablename__ = "badge"
    learner_id = Column(db.Integer, db.ForeignKey('learner.learner_id'), primary_key=True)
    course_id = Column(db.String(255), db.ForeignKey('course.course_id'), primary_key=True)
    is_qualified = Column(db.Boolean)
    
    __mapper_args__ = {
        'polymorphic_identity': 'badge'
    }
    
    def to_dict(self):
        col = self.__mapper__.column_attrs.keys()
        result = {}
        for i in col:
            result[i] = getattr(self, i)
        return result

# quiz_results - for learners (tag to quiz)
class Quiz_Results(db.Model):
    __tablename__ = "quiz_results"
    learner_id = Column(db.Integer, db.ForeignKey("learner.learner_id"), primary_key=True)
    course_id = Column(db.String(255), primary_key=True)
    class_id = Column(db.Integer, primary_key=True)
    quiz_id = Column(db.Integer, primary_key=True)
    score = Column(db.Integer)
    
    __mapper_args__ = {
        'polymorphic_identity': 'quiz_results'
    }
    
    __table_args__ = (
        ForeignKeyConstraint(
            ["course_id", "class_id", "quiz_id"],
            ["quiz.course_id", "quiz.class_id", "quiz.quiz_id"]
        ), {}
    )
    
    def to_dict(self):
        col = self.__mapper__.column_attrs.keys()
        result = {}
        for i in col:
            result[i] = getattr(self, i)
        return result

# material_completion_status - for learners (tag to material)
class Material_Completion_Status(db.Model):
    __tablename__ = "material_completion_status"
    learner_id = Column(db.Integer, db.ForeignKey("learner.learner_id"), primary_key=True)
    course_id = Column(db.String(255), primary_key=True)
    class_id = Column(db.Integer, primary_key=True)
    chapter_id = Column(db.Integer, primary_key=True)
    material_id = Column(db.Integer, primary_key=True)
    is_completed = Column(db.Boolean)
    
    __mapper_args__ = {
        'polymorphic_identity': 'material_completion_status'
    }
    
    __table_args__ = (
        ForeignKeyConstraint(
            ["course_id", "class_id", "chapter_id", "material_id"],
            ["material.course_id", "material.class_id", "material.chapter_id", "material.material_id"]
        ), {}
    ) 
    
    def to_dict(self):
        col = self.__mapper__.column_attrs.keys()
        result = {}
        for i in col:
            result[i] = getattr(self, i)
        return result
