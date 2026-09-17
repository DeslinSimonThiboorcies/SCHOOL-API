from datetime import datetime, timedelta, timezone
from urllib.parse import parse_qs, urlparse

from school.models.password_reset_token import PasswordResetToken


FORGOT_PASSWORD_URL = "/api/auth/forgot-password"
VERIFY_TOKEN_URL = "/api/auth/verify-reset-token"
RESET_PASSWORD_URL = "/api/auth/reset-password"


def reset_token_from(response):
    reset_url = response.get_json()["reset_url"]
    return parse_qs(urlparse(reset_url).query)["token"][0]


class TestPasswordReset:

    def test_create_reset_token(self, client, create_student):
        create_student(email="reset@example.com")

        response = client.post(
            FORGOT_PASSWORD_URL,
            json={
                "email": "RESET@EXAMPLE.COM",
                "account_type": "student",
            },
        )

        assert response.status_code == 200
        assert response.get_json()["message"] == (
            "Password reset link generated"
        )
        assert "token=" in response.get_json()["reset_url"]
        assert response.get_json()["reset_url"].endswith(
            "&account_type=STUDENT"
        )

    def test_forgot_password_unknown_account(self, client):
        response = client.post(
            FORGOT_PASSWORD_URL,
            json={
                "email": "missing@example.com",
                "account_type": "STUDENT",
            },
        )

        assert response.status_code == 404
        assert response.get_json()["message"] == "Account not found"

    def test_verify_reset_token(self, client, create_student):
        create_student(email="verify@example.com")
        create_response = client.post(
            FORGOT_PASSWORD_URL,
            json={
                "email": "verify@example.com",
                "account_type": "STUDENT",
            },
        )

        token = reset_token_from(create_response)
        response = client.post(
            VERIFY_TOKEN_URL,
            json={"token": token, "account_type": "student"},
        )

        assert response.status_code == 200
        assert response.get_json()["message"] == "Reset token is valid"

    def test_reset_password_changes_password(
        self, client, create_student
    ):
        student = create_student(
            email="change@example.com",
            password="oldpassword",
        )
        create_response = client.post(
            FORGOT_PASSWORD_URL,
            json={
                "email": student.email,
                "account_type": "STUDENT",
            },
        )

        token = reset_token_from(create_response)
        response = client.post(
            RESET_PASSWORD_URL,
            json={
                "token": token,
                "account_type": "STUDENT",
                "new_password": "newpassword",
            },
        )

        assert response.status_code == 200
        assert student.verify_students_password("newpassword")
        assert not student.verify_students_password("oldpassword")

    def test_reset_token_cannot_be_reused(self, client, create_student):
        create_student(email="reuse@example.com")
        create_response = client.post(
            FORGOT_PASSWORD_URL,
            json={
                "email": "reuse@example.com",
                "account_type": "STUDENT",
            },
        )
        token = reset_token_from(create_response)

        client.post(
            RESET_PASSWORD_URL,
            json={
                "token": token,
                "account_type": "STUDENT",
                "new_password": "firstnewpassword",
            },
        )
        response = client.post(
            RESET_PASSWORD_URL,
            json={
                "token": token,
                "account_type": "STUDENT",
                "new_password": "secondnewpassword",
            },
        )

        assert response.status_code == 400
        assert response.get_json()["message"] == (
            "Reset token has already been used"
        )

    def test_expired_reset_token_is_rejected(
        self, client, create_student, db
    ):
        student = create_student(email="expired@example.com")
        create_response = client.post(
            FORGOT_PASSWORD_URL,
            json={
                "email": student.email,
                "account_type": "STUDENT",
            },
        )
        token = reset_token_from(create_response)
        reset_record = PasswordResetToken.query.filter_by(
            account_id=student.id,
            account_type="STUDENT",
        ).first()
        reset_record.expires_at = datetime.now(timezone.utc).replace(
            tzinfo=None
        ) - timedelta(minutes=1)
        db.session.commit()

        response = client.post(
            VERIFY_TOKEN_URL,
            json={"token": token, "account_type": "STUDENT"},
        )

        assert response.status_code == 400
        assert response.get_json()["message"] == "Reset token has expired"
from school.test.conftest import auth_headers

def test_forgot_password_missing_fields(client):

    response = client.post(
        "/api/auth/forgot-password",
        json={}
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["message"] == (
        "account_type and email are required"
    )


def test_forgot_password_invalid_account_type(client):

    response = client.post(
        "/api/auth/forgot-password",
        json={
            "account_type": "ADMIN",
            "email": "test@gmail.com"
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["message"] == (
        "account_type must be STUDENT, TEACHER or PRINCIPAL"
    )


def test_verify_reset_token_missing_fields(client):

    response = client.post(
        "/api/auth/verify-reset-token",
        json={}
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["message"] == (
        "token and account_type are required"
    )


def test_verify_invalid_reset_token(client):

    response = client.post(
        "/api/auth/verify-reset-token",
        json={
            "token": "invalid-token",
            "account_type": "STUDENT"
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["message"] == "Invalid reset token"


def test_reset_password_missing_fields(client):

    response = client.post(
        "/api/auth/reset-password",
        json={}
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["message"] == (
        "token, account_type and new_password are required"
    )


def test_reset_password_invalid_token(client):

    response = client.post(
        "/api/auth/reset-password",
        json={
            "token": "invalid-token",
            "account_type": "STUDENT",
            "new_password": "NewPassword123"
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["message"] == "Invalid reset token"