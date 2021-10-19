from flask import Flask, Blueprint

from .todo import todo
from .extensions import db, cors
import pymysql

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

    return app

app = create_app()