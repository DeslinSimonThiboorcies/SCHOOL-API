import pytest
from school.test.conftest import auth_headers


REGISTER_URL = "/api/students/register"
LOGIN_URL = "/api/students/login"
ALL_PROFILE_URL = "/api/students/all_profile"


def my_profile_url(student_id):
    return f"/api/students/my_profile/{student_id}"


def update_url(student_id):
    return f"/api/students/update/{student_id}"


def delete_url(student_id):
    return f"/api/students/delete/{student_id}"


class TestStudentRegistration:

    def test_register_students(
            self, 
            client
        ):

        response = client.post(
            REGISTER_URL, 
            json={
            "name": "New Student",
            "email": "student1@example.com",
            "password": "123456",
        })

        assert response.status_code == 201
        assert response.get_json()["Message"] == "Student Create Successfully"

    def test_duplicate_student(
            self, 
            client, 
            create_student
        ):

        create_student(
            email = "dupstudent@example.com"
        )

        response = client.post(
            REGISTER_URL, 
            json={
            "name": "Another",
            "email": "dupstudent@example.com",
            "password": "123456",
        })

        assert response.status_code == 400

    def test_register_teacher(
            self, 
            client, 
            create_teacher
        ):
        create_teacher(
            email = "shared@example.com"
        )

        response = client.post(
            REGISTER_URL, 
            json={
            "name": "Cross Register",
            "email": "shared@example.com",
            "password": "123456",
        })

        assert response.status_code == 400
        assert "TEACHERS" in response.get_json()["Message"]


class TestStudentLogin:

    def test_login_students(
            self, 
            client, 
            create_student
        ):

        create_student(
            email = "login2@example.com", 
            password = "mypassword"
        )

        response = client.post(
            LOGIN_URL, 
            json={
            "email": "login2@example.com",
            "password": "mypassword",
        })

        assert response.status_code == 200
        assert response.get_json()["TOKEN"]

    def test_login_wrong_password(
            self, 
            client, 
            create_student
        ):

        create_student(
            email = "wrong2@example.com", 
            password = "correct"
        )

        response = client.post(
            LOGIN_URL, 
            json={
            "email": "wrong2@example.com",
            "password": "incorrect",
        })

        assert response.status_code == 401

    def test_login_unknown_email(
            self, 
            client
        ):
        response = client.post(
            LOGIN_URL, 
            json={
            "email": "nobody@example.com",
            "password": "whatever",
        })

        assert response.status_code == 401


class TestAllProfile:

    def test_all_profile(
            self, 
            client
        ):
        
        response = client.get(ALL_PROFILE_URL)
        assert response.status_code == 401

    def test_plain_student(
            self, 
            client, 
            student_token
        ):
        _student, token = student_token

        response = client.get(
            ALL_PROFILE_URL, 
            headers = auth_headers(token)
        )
        assert response.status_code == 403

    def test_teacher_allowed(
            self, 
            client, 
            teacher_token, 
            create_student
        ):
        _teacher, token = teacher_token
        create_student(email = "listed@example.com")

        response = client.get(
            ALL_PROFILE_URL, 
            headers = auth_headers(token)
        )

        assert response.status_code == 200
        assert response.get_json()["MESSAGE"]


class TestMyProfile:

    def test_my_profile(
            self, 
            client, 
            student_token
        ):

        student, token = student_token

        response = client.get(
            my_profile_url(student.id), 
            headers=auth_headers(token)
        )

        assert response.status_code == 200
        assert response.get_json()["MESSAGE"]["email"] == student.email

    def test_other_profile_denied(
            self, 
            client, 
            student_token, 
            create_student
        ):
        _student, token = student_token
        other = create_student(email = "other_student@example.com")

        response = client.get(
            my_profile_url(other.id), 
            headers=auth_headers(token)
        )

        assert response.status_code == 403


class TestUpdateStudent:

    def test_self_update_allowed(
            self, 
            client, 
            student_token
        ):
        student, token = student_token

        response = client.put(
            update_url(student.id),
            json={"name": "Updated Student Name"},
            headers=auth_headers(token),
        )

        assert response.status_code == 200

    def test_update_other_denied(
            self, 
            client, 
            student_token, 
            create_student
        ):
        _student, token = student_token
        other = create_student(email = "target_student@example.com")

        response = client.put(
            update_url(other.id),
            json={"name": "Hacked"},
            headers=auth_headers(token),
        )

        assert response.status_code == 403

    def test_teacher_updates_students(
            self, 
            client, 
            teacher_token, 
            create_student, 
            db
        ):
        teacher, token = teacher_token
        target = create_student(
            name = "Original", 
            email = "target2@example.com"
        )

        response = client.put(
            update_url(target.id),
            json={"name": "Changed By Teacher"},
            headers=auth_headers(token),
        )

        assert response.status_code == 200

        db.session.refresh(target)
        assert target.name == "Changed By Teacher"


class TestDeleteStudent:

    def test_delete_other_denied(
            self, 
            client, 
            student_token, 
            create_student
        ):
        _student, token = student_token
        other = create_student(
            email = "deleteme_student@example.com"
        )

        response = client.delete(delete_url(other.id), headers=auth_headers(token))

        assert response.status_code == 403

    def test_teacher_can_delete(
            self, 
            client, 
            teacher_token, 
            create_student, 
            db
        ):
        _teacher, token = teacher_token
        target = create_student(email = "deleteme_student2@example.com")
        target_id = target.id

        response = client.delete(delete_url(target_id), headers=auth_headers(token))

        assert response.status_code == 200
        from school.models.students import Student
        assert db.session.get(Student, target_id) is None

    def test_delete_nonexistent_student(
            self, 
            client, 
            teacher_token
        ):
        _teacher, token = teacher_token

        response = client.delete(delete_url(999999), headers=auth_headers(token))

        assert response.status_code == 404