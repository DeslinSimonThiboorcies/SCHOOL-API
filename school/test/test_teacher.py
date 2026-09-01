from school.test.conftest import auth_headers


REGISTER_URL = "/api/teacher/register"
LOGIN_URL = "/api/teacher/login"
VIEW_ALL_URL = "/api/teacher/view_all"


def single_profile_url(teacher_id):
    return f"/api/teacher/single_profile/{teacher_id}"


def update_url(teacher_id):
    return f"/api/teacher/update/{teacher_id}"


def delete_url(teacher_id):
    return f"/api/teacher/delete/{teacher_id}"


class TestTeacherRegistration:

    def test_register_success(self, client):
        response = client.post(
            REGISTER_URL, 
            json={
            "name": "Test User",
            "department": "Commerces",
            "email": "new.teacher@example.com",
            "password": "123456",
        })

        assert response.status_code == 201
        assert response.get_json()["MESSAGE"] == "TEACHER CREATE SUCCESSFULLY"

    def test_register_duplicate_teacher(
            self, 
            client, 
            create_teacher
        ):
        create_teacher(email="dup@example.com")

        response = client.post(
            REGISTER_URL, 
            json={
            "name": "Someone Else",
            "department": "Science",
            "email": "dup@example.com",
            "password": "123456",
        })

        assert response.status_code == 400
        assert "ALREADY EXIST" in response.get_json()["MESSAGE"]


class TestTeacherLogin:

    def test_login_success(
            self, 
            client, 
            create_teacher
        ):
        create_teacher(
            email = "login@example.com", 
            password = "mypassword"
        )

        response = client.post(
            LOGIN_URL, 
            json={
            "email": "login@example.com",
            "password": "mypassword",
        })

        assert response.status_code == 200
        body = response.get_json()
        assert body["MESSAGE"] == "LOGIN SUCCESSFULLY"
        assert body["TOKEN"]

    def test_login_wrong_password(
            self, 
            client, 
            create_teacher
        ):
        create_teacher(
            email = "wrongpass@example.com",
            password = "correct"
        )

        response = client.post(
            LOGIN_URL, 
            json={
            "email": "wrongpass@example.com",
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
            "email": "ghost@example.com",
            "password": "whatever",
        })

        assert response.status_code == 401


class TestViewAllTeachers:

    def test_view_all_teachers(self, client):
        response = client.get(VIEW_ALL_URL)
        assert response.status_code == 401

    def test_plain_teacher(
            self, 
            client, 
            teacher_token
        ):
        _teacher, token = teacher_token

        response = client.get(
            VIEW_ALL_URL, 
            headers=auth_headers(token)
        )
        assert response.status_code == 403

    def test_principal_allowed(
            self, 
            client, 
            principal_token, 
            create_teacher
        ):
        _principal, token = principal_token
        create_teacher(
            name = "Another", 
            email = "another@example.com"
        )

        response = client.get(
            VIEW_ALL_URL, 
            headers=auth_headers(token)
        )

        assert response.status_code == 200
        assert response.get_json()["MESSAGE"]


class TestSingleProfile:

    def test_self_access_allowed(
            self, 
            client, 
            teacher_token
        ):
        teacher, token = teacher_token

        response = client.get(
            single_profile_url(teacher.id), 
            headers=auth_headers(token)
        )

        assert response.status_code == 200
        assert response.get_json()["MESSAGE"]["email"] == teacher.email

    def test_other_profile_denied_for_non_principal(
            self, 
            client, 
            teacher_token, 
            create_teacher
        ):
        _teacher, token = teacher_token
        other = create_teacher(
            name = "Other", 
            email = "other@example.com"
        )

        response = client.get(
            single_profile_url(other.id), 
            headers=auth_headers(token)
        )

        assert response.status_code == 403

    def test_other_profile_allowed_for_principal(
            self, 
            client, 
            principal_token, 
            create_teacher
        ):
        _principal, token = principal_token
        other = create_teacher(
            name="Other", 
            email="other2@example.com"
        )

        response = client.get(
            single_profile_url(other.id), 
            headers=auth_headers(token)
        )

        assert response.status_code == 200


class TestUpdateTeacher:

    def test_self_update_allowed(
            self, 
            client, 
            teacher_token
        ):
        teacher, token = teacher_token

        response = client.put(
            update_url(teacher.id),
            json={"name": "Updated Name"},
            headers=auth_headers(token),
        )

        assert response.status_code == 200
        assert response.get_json()["MESSAGE"] == "TEACHER UPDATE SUCCESS"

    def test_update_other_denied_for_non_principal(
            self, 
            client, 
            teacher_token, 
            create_teacher
        ):
        _teacher, token = teacher_token
        other = create_teacher(email="other3@example.com")

        response = client.put(
            update_url(other.id),
            json={"name": "Hacked Name"},
            headers=auth_headers(token),
        )

        assert response.status_code == 403

    def test_principal_updates_target(
            self, 
            client, 
            principal_token, 
            create_teacher, 
            db
        ):

        principal, token = principal_token
        target = create_teacher(
            name = "Original Name", 
            email = "target@example.com"
        )

        response = client.put(
            update_url(target.id),
            json={"name": "Changed By Principal"},
            headers=auth_headers(token),
        )

        assert response.status_code == 200

        db.session.refresh(target)
        db.session.refresh(principal)
        assert target.name == "Changed By Principal"
        assert principal.name != "Changed By Principal"

    def test_update_nonexistent_teacher(
            self, 
            client, 
            principal_token
        ):
        _principal, token = principal_token

        response = client.put(
            update_url(999999),
            json={"name": "Ghost"},
            headers=auth_headers(token),
        )

        assert response.status_code == 404


class TestDeleteTeacher:

    def test_delete_other_denied(
            self, 
            client, 
            teacher_token, 
            create_teacher
        ):
        _teacher, token = teacher_token
        other = create_teacher(email="deleteme@example.com")

        response = client.delete(delete_url(other.id), headers=auth_headers(token))

        assert response.status_code == 403

    def test_principal_can_delete(
            self, 
            client, 
            principal_token, 
            create_teacher, 
            db
        ):
        _principal, token = principal_token
        target = create_teacher(email="deleteme2@example.com")
        target_id = target.id

        response = client.delete(delete_url(target_id), headers=auth_headers(token))

        assert response.status_code == 200
        from school.models.teacher import Teacher
        assert db.session.get(Teacher, target_id) is None

    def test_delete_nonexistent_teacher_404(
            self, 
            client, 
            principal_token
        ):
        token = principal_token

        response = client.delete(delete_url(999999), headers=auth_headers(token))

        assert response.status_code == 422