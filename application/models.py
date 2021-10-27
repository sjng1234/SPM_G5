from .extensions import db
from sqlalchemy.sql.schema import Column

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

#Course
class Course(db.Model):
    __tablename__ = "course"
    course_id = Column(db.String(50), primary_key=True)
    course_name = Column(db.String(255))
    course_description = Column(db.String(255))
    course_creator_id = Column(db.String(255))
    date_created =  Column(db.DateTime)
    
    __mapper_args__ = {
        'polymorphic_identity': 'courseitem'
    }

    def __repr__(self):
        return f"{self.course_id}"

    def to_dict(self):
        col = self.__mapper__.column_attrs.keys()
        result = {}
        for i in col:
            result[i] = getattr(self, i)
        return result

#Class
class Class(db.Model):
    __tablename__ = "class"
    course_id = Column(db.String(50), primary_key=True)
    class_id = Column(db.Integer, primary_key=True)
    class_creator_id = Column(db.String(255))
    start_datetime = Column(db.DateTime)
    end_datetime = Column(db.DateTime)
    class_size = Column(db.Integer)
    trainer_id = Column(db.Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'courseitem'
    }

    def __repr__(self):
        return f"{self.course_id} {self.class_id}"

    def to_dict(self):
        col = self.__mapper__.column_attrs.keys()
        result = {}
        for i in col:
            result[i] = getattr(self, i)
        return result