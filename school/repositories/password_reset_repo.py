from datetime import datetime, timezone
from school.extensison.db import db
from school.models.password_reset_token import PasswordResetToken


class PasswordResetRepository:

    @staticmethod
    def create(reset_token):
        db.session.add(reset_token)
        db.session.commit()
        return reset_token

    @staticmethod
    def get_by_token_hash(token_hash):
        return PasswordResetToken.query.filter_by(
            token_hash=token_hash
        ).first()

    @staticmethod
    def get_active_tokens(account_type, account_id):
        return PasswordResetToken.query.filter(
            PasswordResetToken.account_type == account_type,
            PasswordResetToken.account_id == account_id,
            PasswordResetToken.used_at.is_(None),
            PasswordResetToken.expires_at > datetime.now(
                timezone.utc
            ).replace(tzinfo=None)
        ).all()

    @staticmethod
    def mark_as_used(reset_token):
        reset_token.used_at = datetime.now(
            timezone.utc
        ).replace(tzinfo=None)
        db.session.commit()
        return reset_token

    @staticmethod
    def invalidate_active_tokens(account_type, account_id):

        active_tokens = PasswordResetRepository.get_active_tokens(
            account_type,
            account_id
        )

        for reset_token in active_tokens:
            reset_token.used_at = datetime.now(
                timezone.utc
            ).replace(tzinfo=None)

        db.session.commit()