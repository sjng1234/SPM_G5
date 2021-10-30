from enum import unique
from .extensions import db
from sqlalchemy.sql.schema import Column, ForeignKey, ForeignKeyConstraint, PrimaryKeyConstraint

# Model
# example
class Todo(db.Model):
    __tablename__ = "TODOS"
    id = Column(db.Integer, primary_key=True)
    title = Column(db.String(20))
    todo_description = Column(db.String(100))

    __mapper_args__ = {
        'polymorphic_identity': 'todoitem'
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
    course_creator_id = Column(db.String(255))
    date_created =  Column(db.DateTime)

    db.UniqueConstraint('course_id')
    
    __mapper_args__ = {
        'polymorphic_identity': 'course'
    }

    def __repr__(self):
        return f"CourseID:{self.course_id}"

    def to_dict(self):
        col = self.__mapper__.column_attrs.keys()
        result = {}
        for i in col:
            result[i] = getattr(self, i)
        return result
class Class(Course):
    __tablename__ = "class"
    course_id = Column(db.String(50), db.ForeignKey('course.course_id'),primary_key=True)
    class_id = Column(db.Integer, primary_key=True)
    course_name = Column(db.String(255))
    course_description = Column(db.String(255))
    course_creator_id = Column(db.String(255))
    date_created =  Column(db.DateTime)


    db.UniqueConstraint('class_id')
    
    __mapper_args__ = {
        'polymorphic_identity': 'class'
    }

    def __repr__(self):
        return f"New Class: {self.course_id,self.class_id} - {self.course_name}"

    def to_dict(self):
        col = self.__mapper__.column_attrs.keys()
        result = {}
        for i in col:
            result[i] = getattr(self, i)
        return result
class Quiz(Class):
    __tablename__ = "quiz"
    course_id = Column(db.String(50), db.ForeignKey('class.course_id'),primary_key=True)
    class_id = Column(db.Integer,db.ForeignKey('class.class_id'), primary_key=True)
    quiz_id = Column(db.Integer, primary_key=True)
    duration = Column(db.Integer)

    db.UniqueConstraint('quiz_id')
    
    __mapper_args__ = {
        'polymorphic_identity': 'quiz'
    }

    def __repr__(self):
        return f"Quiz:{self.class_id,self.quiz_id}"

    def to_dict(self):
        col = self.__mapper__.column_attrs.keys()
        result = {}
        for i in col:
            result[i] = getattr(self, i)
        return result
class Quiz_Questions(Class):
    __tablename__ = "quiz_questions"
    course_id = Column(db.String(50), db.ForeignKey('quiz.course_id'),primary_key=True)
    class_id = Column(db.Integer,db.ForeignKey('quiz.class_id'), primary_key=True)
    quiz_id = Column(db.Integer, db.ForeignKey('quiz.quiz_id'), primary_key=True)
    question_id = Column(db.Integer, primary_key=True)
    question_description = Column(db.String(255))
    answer_course_id = Column(db.Integer, db.ForeignKey('quiz_questions_options.course_id'))
    answer_class_id = Column(db.Integer, db.ForeignKey('quiz_questions_options.class_id'))
    answer_quiz_id = Column(db.Integer, db.ForeignKey('quiz_questions_options.quiz_id'))
    answer_question_id = Column(db.Integer, db.ForeignKey('quiz_questions_options.question_id'))
    answer_option = Column(db.String(255), db.ForeignKey('quiz_questions_options.option'))

    db.UniqueConstraint('quiz_id')
    
    __mapper_args__ = {
        'polymorphic_identity': 'quiz_questions'
    }

    def __repr__(self):
        return f"Quiz_Questions: {self.class_id, self.quiz_id, self.question_id}"

    def to_dict(self):
        col = self.__mapper__.column_attrs.keys()
        result = {}
        for i in col:
            result[i] = getattr(self, i)
        return result

    def get_course_name(self):
        return getattr(self, "course_name")

# Classes
class Classes(Course):
    __tablename__ = "classes"
    course_id = Column(db.String(50), db.ForeignKey("course.course_id"), primary_key = True)
    class_id = Column(db.Integer, primary_key=True)
    class_creator_id = Column(db.String(255))
    start_datetime = Column(db.DateTime)
    end_datetime = Column(db.DateTime)
    class_size = Column(db.Integer)
    trainer_id = Column(db.Integer)

    def to_dict(self):
        col = self.__mapper__.column_attrs.keys()
        result = {}
        for i in col:
            result[i] = getattr(self, i)
        return result

class Chapter(Class):
    __tablename__ = "chapter"
    course_id = Column(db.String(50), db.ForeignKey("class.course_id"), primary_key=True)
    class_id = Column(db.Integer, db.ForeignKey("class.class_id"), primary_key=True)
    chapter_id = Column(db.Integer, primary_key=True)
    chapter_name = Column(db.String(255))
    fk = ForeignKeyConstraint([course_id], [class_id])


    __mapper_args__ = {
        'polymorphic_identity': 'chapteritem'
    }

    __table_args__ = (
        ForeignKeyConstraint(
            ["class.class_id", "class.course_id"]
        ),
    )

    def __repr__ (self):
        return f"{self.chapter_name}"

    def to_dict(self):
        col = self.__mapper__.column_attrs.keys()
        result = {}
        for i in col:
            result[i] = getattr(self, i)
        return result
