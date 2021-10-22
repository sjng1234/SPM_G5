from .extensions import db
from sqlalchemy.sql.schema import Column

# Model

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

class Course(db.Model):
    __tablename__ = "course"
    course_id = Column(db.String(20), primary_key=True)
    course_name = Column(db.String(20))
    course_description = Column(db.String(100))
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