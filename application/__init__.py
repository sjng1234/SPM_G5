from flask import Flask, Blueprint

from .todo import todo
from .course import course
from .classes import classes
from .chapter import chapter
from .quiz import quiz
from .extensions import db, cors
import pymysql
pymysql.install_as_MySQLdb()

def create_app(config_file="settings.py"):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    db.init_app(app)

    cors.init_app(app)

    main = Blueprint('main',__name__)

    @main.route('/')
    def sanity_check():
        return "Blueprint End point"

    app.register_blueprint(main)
    app.register_blueprint(todo)
    app.register_blueprint(course)
    app.register_blueprint(classes)
    app.register_blueprint(chapter)
    app.register_blueprint(quiz)

    return app

app = create_app()