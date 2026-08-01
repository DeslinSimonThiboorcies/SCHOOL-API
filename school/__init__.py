from flask import Flask
from school.config import Config
from school.extensison.db import db
from school.extensison.jwt import jwt

app = Flask(__name__)

def create_app():

    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    from school.route.students_route import student_bp

    app.register_blueprint(
        student_bp,
        url_prefix = "/api"
    )

    from school.route.teacher_services import teach_bp

    app.register_blueprint(
        teach_bp,
        url_prefix = "/api"
    )

    return app