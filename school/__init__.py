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

    from school.route.user_route import user_bp
    app.register_blueprint(
        user_bp,
        url_prefix = "/api"
    )

    from school.route.teacher_route import teacher_bp
    app.register_blueprint(
        teacher_bp,
        url_prefix = "/api"
    )

    from school.route.students_route import student_bp
    app.register_blueprint(
        student_bp,
        url_prefix = "/api"
    )

    from school.route.class_route import class_bp
    app.register_blueprint(
        class_bp,
        url_prefix = "/api"
    )

    from school.route.attendance_route import attendance_bp
    app.register_blueprint(
        attendance_bp,
        url_prefix = "/api"
    )

    from school.route.class_subject_route import class_subject_bp
    app.register_blueprint(
        class_subject_bp,
        url_prefix = "/api"
    )

    from school.route.subject_route import subject_bp
    app.register_blueprint(
        subject_bp
    )

    from school.route.marks_route import marks_bp
    app.register_blueprint(
        marks_bp,
        url_prefix = "/api"
    )

    from school.route.fee_route import fee_bp
    app.register_blueprint(
        fee_bp
    )

    from school.route.timetable_route import timetable_bp
    app.register_blueprint(
        timetable_bp,
        url_prefix="/api"
    )

    from school.route.password_reset_route import password_reset_bp
    app.register_blueprint(
        password_reset_bp
    )

    return app