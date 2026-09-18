from datetime import date

from school.models.users import User
from school.test.conftest import auth_headers


REGISTER_URL = "/api/student/profile"
ALL_STUDENTS_URL = "/api/view/profile"


def profile_url(student_id):
    return f"/api/student/profile/{student_id}"


def update_url(student_id):
    return f"/api/update/student/profile/{student_id}"


def delete_url(student_id):
    return f"/api/delete/student/profile/{student_id}"


def create_unprofiled_user(db, email="unprofiled@example.com"):
    user = User(
        full_name="Unprofiled User",
        email=email,
        date_of_birth=date(2000, 1, 1),
        role="STUDENT",
    )
    user.users_password("password123")
    db.session.add(user)
    db.session.commit()
    return user


class TestStudentProfiles:

    def test_create_student_profile(self, client, db, principal_token):
        _principal, token = principal_token
        user = create_unprofiled_user(db)

        response = client.post(
            REGISTER_URL,
            json={
                "user_id": user.id,
                "admission_number": "ADM-NEW",
                "class_id": 1,
                "parent_name": "Parent Name",
                "parent_phone": "1234567890",
            },
            headers=auth_headers(token),
        )

        assert response.status_code == 201
        assert response.get_json()["student"]["user_id"] == user.id

    def test_create_student_requires_principal_or_teacher(
        self, client, student_token, db
    ):
        _student, token = student_token
        user = create_unprofiled_user(db, email="blocked@example.com")

        response = client.post(
            REGISTER_URL,
            json={
                "user_id": user.id,
                "admission_number": "ADM-BLOCKED",
                "class_id": 1,
                "parent_name": "Parent Name",
                "parent_phone": "1234567890",
            },
            headers=auth_headers(token),
        )

        assert response.status_code == 403

    def test_student_can_view_own_profile(self, client, student_token):
        student, token = student_token

        response = client.get(
            profile_url(student.id),
            headers=auth_headers(token),
        )

        assert response.status_code == 200
        assert response.get_json()["student"]["id"] == student.id

    def test_student_cannot_view_another_profile(
        self, client, student_token, create_student
    ):
        _student, token = student_token
        other = create_student(email="other-student@example.com")

        response = client.get(
            profile_url(other.id),
            headers=auth_headers(token),
        )

        assert response.status_code == 403

    def test_teacher_can_view_all_students(
        self, client, teacher_token, create_student
    ):
        _teacher, token = teacher_token
        create_student(email="listed-student@example.com")

        response = client.get(
            ALL_STUDENTS_URL,
            headers=auth_headers(token),
        )

        assert response.status_code == 200
        assert response.get_json()["students"]

    def test_student_can_update_own_profile(self, client, student_token, db):
        student, token = student_token

        response = client.put(
            update_url(student.id),
            json={"parent_name": "Updated Parent"},
            headers=auth_headers(token),
        )

        assert response.status_code == 200
        db.session.refresh(student)
        assert student.parent_name == "Updated Parent"

    def test_principal_can_delete_student(
        self, client, principal_token, create_student, db
    ):
        _principal, token = principal_token
        student = create_student(email="delete-student@example.com")

        response = client.delete(
            delete_url(student.id),
            headers=auth_headers(token),
        )

        assert response.status_code == 200
        assert db.session.get(type(student), student.id) is None
