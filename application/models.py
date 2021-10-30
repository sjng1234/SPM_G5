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

# Chapter
class Chapter(db.Model):
    __tablename__ = "chapter"
    course_id = Column(db.String(50), primary_key=True)
    class_id = Column(db.Integer, primary_key=True)
    chapter_id = Column(db.Integer, primary_key=True)
    chapter_name = Column(db.String(255))

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
