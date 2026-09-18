from datetime import date

from school.models.users import User
from school.test.conftest import auth_headers


REGISTER_URL = "/api/teachers/profile"
ALL_TEACHERS_URL = "/api/teacher/profile"


def profile_url(teacher_id):
    return f"/api/teacher/{teacher_id}"


def update_url(teacher_id):
    return f"/api/update/department/{teacher_id}"


def delete_url(teacher_id):
    return f"/api/delete/department/{teacher_id}"


def create_unprofiled_user(db, email="unprofiled-teacher@example.com"):
    user = User(
        full_name="Unprofiled Teacher",
        email=email,
        date_of_birth=date(1980, 1, 1),
        role="TEACHER",
    )
    user.users_password("password123")
    db.session.add(user)
    db.session.commit()
    return user


class TestTeacherProfiles:

    def test_create_teacher_profile(self, client, db, principal_token):
        _principal, token = principal_token
        user = create_unprofiled_user(db)

        response = client.post(
            REGISTER_URL,
            json={
                "user_id": user.id,
                "employee_number": "EMP-NEW",
                "department": "Science",
                "qualification": "Education",
            },
            headers=auth_headers(token),
        )

        assert response.status_code == 201
        assert response.get_json()["teacher"]["user_id"] == user.id

    def test_teacher_list_requires_principal(self, client, teacher_token):
        _teacher, token = teacher_token

        response = client.get(
            ALL_TEACHERS_URL,
            headers=auth_headers(token),
        )

        assert response.status_code == 403

    def test_principal_can_list_teachers(
        self, client, principal_token, create_teacher
    ):
        _principal, token = principal_token
        create_teacher(email="listed-teacher@example.com")

        response = client.get(
            ALL_TEACHERS_URL,
            headers=auth_headers(token),
        )

        assert response.status_code == 200
        assert response.get_json()["teachers"]

    def test_teacher_can_view_own_profile(self, client, teacher_token):
        teacher, token = teacher_token

        response = client.get(
            profile_url(teacher.id),
            headers=auth_headers(token),
        )

        assert response.status_code == 200
        assert response.get_json()["teacher"]["id"] == teacher.id

    def test_teacher_cannot_view_another_profile(
        self, client, teacher_token, create_teacher
    ):
        _teacher, token = teacher_token
        other = create_teacher(email="other-teacher@example.com")

        response = client.get(
            profile_url(other.id),
            headers=auth_headers(token),
        )

        assert response.status_code == 403

    def test_teacher_can_update_own_profile(self, client, teacher_token, db):
        teacher, token = teacher_token

        response = client.put(
            update_url(teacher.id),
            json={"department": "Updated Department"},
            headers=auth_headers(token),
        )

        assert response.status_code == 200
        db.session.refresh(teacher)
        assert teacher.department == "Updated Department"

    def test_principal_can_delete_teacher(
        self, client, principal_token, create_teacher, db
    ):
        _principal, token = principal_token
        teacher = create_teacher(email="delete-teacher@example.com")

        response = client.delete(
            delete_url(teacher.id),
            headers=auth_headers(token),
        )

        assert response.status_code == 200
        assert db.session.get(type(teacher), teacher.id) is None
