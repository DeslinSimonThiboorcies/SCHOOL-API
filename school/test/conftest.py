import pytest
from datetime import date

from school import create_app
from school.config import TestConfig
from school.extensison.db import db as _db
from school.models.student_profiles import Student
from school.models.teacher_profile import Teacher
from school.models.users import User
from school.models.class_model import ClassModel

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
        _db.engine.dispose()


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
        user = User(
            full_name=name,
            email=email,
            date_of_birth=date(2000, 1, 1),
            role=role,
        )
        user.users_password(password)
        db.session.add(user)
        db.session.flush()

        student = Student(
            user_id=user.id,
            admission_number=f"ADM-{user.id}",
            class_id=1,
            parent_name="Test Parent",
            parent_phone="1234567890",
        )
        student.email = email
        student.name = name
        student.verify_students_password = user.verify_users_password
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

        user = User(
            full_name=name,
            email=email,
            date_of_birth=date(1980, 1, 1),
            role=role,
        )
        user.users_password(password)
        db.session.add(user)
        db.session.flush()

        teacher = Teacher(
            user_id=user.id,
            employee_number=f"EMP-{user.id}",
            department=department,
            qualification="Education",
        )
        teacher.email = email
        teacher.name = name
        teacher.set_teachers_password = user.users_password
        teacher.check_teachers_password = user.verify_users_password
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
            identity=str(student.user_id),
            additional_claims={"role": "STUDENT"}
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
            identity=str(teacher.user_id),
            additional_claims={"role": "TEACHER"}
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
            identity=str(principal.user_id),
            additional_claims={"role": "PRINCIPAL"}
        )
    return principal, token


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def principal_headers(principal_token):
    _principal, token = principal_token
    return auth_headers(token)


@pytest.fixture
def teacher_headers(teacher_token):
    _teacher, token = teacher_token
    return auth_headers(token)


@pytest.fixture
def student_headers(student_token):
    _student, token = student_token
    return auth_headers(token)
