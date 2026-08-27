import pytest

from school import create_app
from school.config import TestConfig
from school.extensison.db import db as _db
from school.models.students import Student
from school.models.teacher import Teacher

from flask_jwt_extended import create_access_token


@pytest.fixture
def app():

    application = create_app(
        config_class = TestConfig
    )

    with application.app_context():
        _db.create_all()
        yield application
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    return _db


@pytest.fixture
def create_student(db):
    def register_student(
        name = "Test Student", 
        email = "student@example.com",
        password = "password123", 
        role = "STUDENT", 
        department = "COMMERCES"
    ):
        student = Student(
            name = name, 
            email = email, 
            role = role, 
            department = department
        )

        student.students_password(password)
        db.session.add(student)
        db.session.commit()
        return student
    return register_student


@pytest.fixture
def create_teacher(db):

    def register_teacher(
        name = "Test Teacher", 
        email = "teacher@example.com",
        password = "password123", 
        role = "TEACHER", 
        department = "COMMERCES"
        ):

        teacher = Teacher(
            name = name, 
            email = email, 
            role = role, 
            department = department
        )

        teacher.set_teachers_password(password)
        db.session.add(teacher)
        db.session.commit()
        return teacher
    return register_teacher


@pytest.fixture
def student_token(
    app, 
    create_student
    ):

    student = create_student()
    with app.app_context():
        token = create_access_token(
            identity=str(student.id)
        )
    return student, token

@pytest.fixture
def teacher_token(
    app, 
    create_teacher
    ):

    teacher = create_teacher()
    with app.app_context():
        token = create_access_token(
            identity=str(teacher.id)
        )
    return teacher, token


@pytest.fixture
def principal_token(
    app, 
    create_teacher
    ):

    principal = create_teacher(
        name = "Principal", 
        email = "principal@example.com", 
        role = "PRINCIPAL"
    )

    with app.app_context():
        token = create_access_token(
            identity=str(principal.id)
        )
    return principal, token


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}
