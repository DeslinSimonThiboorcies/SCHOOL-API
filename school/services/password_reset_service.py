import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from flask import current_app

from school.models.password_reset_token import PasswordResetToken
from school.repositories.password_reset_repo import PasswordResetRepository

from school.repositories.students_repo import StudentsRepository
from school.repositories.teacher_repo import TeacherRepository


class PasswordResetService:

    RESET_TOKEN_EXPIRY_MINUTES = 15

    @staticmethod
    def _hash_token(raw_token):

        return hashlib.sha256(
            raw_token.encode("utf-8")
        ).hexdigest()

    @staticmethod
    def _find_account(account_type, email):

        if account_type == "STUDENT":
            return StudentsRepository.read_mail(email)

        if account_type == "TEACHER":
            return TeacherRepository.teacher_mail(email)

        if account_type == "PRINCIPAL":
            return TeacherRepository.teacher_mail(email)

        return None

    @staticmethod
    def _find_account_by_id(account_type, account_id):

        if account_type == "STUDENT":
            return StudentsRepository.read_id(account_id)

        if account_type == "TEACHER":
            return TeacherRepository.view_teacher(account_id)

        if account_type == "PRINCIPAL":
            return TeacherRepository.view_teacher(account_id)

        return None

    @staticmethod
    def create_reset_token(account_type, email):

        account_type = account_type.upper().strip()
        email = email.lower().strip()

        account = PasswordResetService._find_account(
            account_type=account_type,
            email=email
        )

        if not account:
            raise ValueError("Account not found")

        PasswordResetRepository.invalidate_active_tokens(
            account_type=account_type,
            account_id=account.id
        )

        raw_token = secrets.token_urlsafe(32)

        token_hash = PasswordResetService._hash_token(
            raw_token
        )

        expires_at = datetime.now(timezone.utc).replace(
            tzinfo=None
        ) + timedelta(
            minutes=PasswordResetService.RESET_TOKEN_EXPIRY_MINUTES
        )

        reset_token = PasswordResetToken(
            account_type=account_type,
            account_id=account.id,
            token_hash=token_hash,
            expires_at=expires_at
        )

        PasswordResetRepository.create(reset_token)

        reset_url = (
            f"{current_app.config['PASSWORD_RESET_URL']}"
            f"?token={raw_token}"
            f"&account_type={account_type}"
        )

        return {
            "message": "Password reset link generated",
            "reset_url": reset_url,
            "expires_at": expires_at
        }

    @staticmethod
    def verify_reset_token(raw_token, account_type):

        if not raw_token:
            raise ValueError("Reset token is required")

        account_type = account_type.upper().strip()

        if account_type not in [
            "STUDENT",
            "TEACHER",
            "PRINCIPAL"
        ]:
            raise ValueError("Invalid account type")

        token_hash = PasswordResetService._hash_token(
            raw_token
        )

        reset_token = PasswordResetRepository.get_by_token_hash(
            token_hash
        )

        if not reset_token:
            raise ValueError("Invalid reset token")

        if reset_token.account_type != account_type:
            raise ValueError("Invalid reset token")

        if reset_token.used_at is not None:
            raise ValueError("Reset token has already been used")

        if reset_token.expires_at <= datetime.now(
            timezone.utc
        ).replace(tzinfo=None):
            raise ValueError("Reset token has expired")

        return reset_token

    @staticmethod
    def reset_password(raw_token, account_type, new_password):

        if not new_password:
            raise ValueError("New password is required")

        if len(new_password) < 8:
            raise ValueError(
                "Password must be at least 8 characters"
            )

        reset_token = PasswordResetService.verify_reset_token(
            raw_token=raw_token,
            account_type=account_type
        )

        account = PasswordResetService._find_account_by_id(
            account_type=reset_token.account_type,
            account_id=reset_token.account_id
        )

        if not account:
            raise ValueError("Account not found")

        if reset_token.account_type == "STUDENT":
            account.students_password(new_password)
        else:
            account.set_teachers_password(new_password)

        PasswordResetRepository.mark_as_used(reset_token)

        return {
            "message": "Password reset successfully"
        }