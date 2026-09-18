from datetime import date

from school.models.users import User
from school.test.conftest import auth_headers


REGISTER_URL = "/api/user/register"
LOGIN_URL = "/api/user/login"
PROFILE_URL = "/api/profile"
ALL_USERS_URL = "/api/all_users/profile"


def user_payload(email="user@example.com", role="STUDENT"):
    return {
        "full_name": "Test User",
        "email": email,
        "phone_number": "1234567890",
        "date_of_birth": "2000-01-01",
        "password": "password123",
        "role": role,
    }


def create_user(db, email="user@example.com", role="STUDENT"):
    phone_number = f"555{abs(hash(email)) % 10000000:07d}"
    user = User(
        full_name="Test User",
        email=email,
        phone_number=phone_number,
        date_of_birth=date(2000, 1, 1),
        role=role,
    )
    user.users_password("password123")
    db.session.add(user)
    db.session.commit()
    return user


class TestUserRegistration:

    def test_register_user(self, client):
        response = client.post(
            REGISTER_URL,
            json=user_payload("new@example.com")
        )

        assert response.status_code == 201
        body = response.get_json()
        assert body["message"] == "User registered successfully"
        assert body["user"]["email"] == "new@example.com"

    def test_register_user_rejects_duplicate_email(self, client, db):
        create_user(db, email="duplicate@example.com")

        response = client.post(
            REGISTER_URL,
            json=user_payload("duplicate@example.com")
        )

        assert response.status_code == 400
        assert response.get_json()["message"] == "USER ALREADY EXIST!"

    def test_register_user_validates_required_fields(self, client):
        response = client.post(
            REGISTER_URL,
            json={"email": "invalid@example.com"}
        )

        assert response.status_code == 400
        assert response.get_json()["message"] == "Validation failed"


class TestUserLogin:

    def test_login_returns_access_token(self, client, db):
        create_user(db, email="login@example.com")

        response = client.post(
            LOGIN_URL,
            json={
                "email": "login@example.com",
                "password": "password123",
            }
        )

        assert response.status_code == 200
        assert response.get_json()["message"] == "Login successful"
        assert response.get_json()["access_token"]

    def test_login_rejects_invalid_password(self, client, db):
        create_user(db, email="wrong-password@example.com")

        response = client.post(
            LOGIN_URL,
            json={
                "email": "wrong-password@example.com",
                "password": "incorrect-password",
            }
        )

        assert response.status_code == 401
        assert response.get_json()["message"] == "INVALID PASSWORD OR EMAIL"


class TestUserProfiles:

    def test_user_can_view_own_profile(self, client, db):
        user = create_user(db, email="profile@example.com")
        from flask_jwt_extended import create_access_token

        token = create_access_token(
            identity=str(user.id),
            additional_claims={"role": user.role}
        )

        response = client.get(
            PROFILE_URL,
            headers=auth_headers(token)
        )

        assert response.status_code == 200
        assert response.get_json()["email"] == user.email

    def test_principal_can_view_all_users(self, client, db):
        principal = create_user(
            db,
            email="principal@example.com",
            role="PRINCIPAL"
        )
        create_user(db, email="listed@example.com")
        from flask_jwt_extended import create_access_token

        token = create_access_token(
            identity=str(principal.id),
            additional_claims={"role": "PRINCIPAL"}
        )

        response = client.get(
            ALL_USERS_URL,
            headers=auth_headers(token)
        )

        assert response.status_code == 200
        assert len(response.get_json()["users"]) == 2

    def test_student_cannot_view_all_users(self, client, db):
        student = create_user(db, email="student@example.com")
        from flask_jwt_extended import create_access_token

        token = create_access_token(
            identity=str(student.id),
            additional_claims={"role": "STUDENT"}
        )

        response = client.get(
            ALL_USERS_URL,
            headers=auth_headers(token)
        )

        assert response.status_code == 403
