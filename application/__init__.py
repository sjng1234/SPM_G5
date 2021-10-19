from flask import Flask, Blueprint

from .todo import todo
from .extensions import db, cors
import pymysql

def create_app(config_file="settings.py"):
    application = Flask(__name__)

    application.config.from_pyfile(config_file)

    db.init_app(application)

    cors.init_app(application)

    main = Blueprint('main',__name__)

    @main.route('/')
    def sanity_check():
        return "Blueprint End point"

    application.register_blueprint(main)
    application.register_blueprint(todo)

    return application

application = create_app()