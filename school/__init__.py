from flask import Flask
from school.config import Config
from school.extensison.db import db
from school.extensison.jwt import jwt


def create_app(config_class=Config, config_overrides=None):

    app = Flask(__name__)
    app.config.from_object(config_class)

    if config_overrides:
        app.config.update(config_overrides)

    db.init_app(app)
    jwt.init_app(app)

    from school.route.students_route import student_bp

    app.register_blueprint(
        student_bp,
        url_prefix = "/api"
    )

    from school.route.teacher_route import teach_bp

    app.register_blueprint(
        teach_bp,
        url_prefix = "/api"
    )

    return app