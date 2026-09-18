from school.extensison.db import db
from school.models.password_reset_token import PasswordResetToken


class PasswordResetRepository:

    @staticmethod
    def invalidate_active_tokens(account_type, account_id):
        PasswordResetToken.query.filter_by(
            account_type=account_type,
            account_id=account_id,
            used_at=None
        ).update({
            PasswordResetToken.used_at: db.func.now()
        })
        db.session.commit()

    @staticmethod
    def get_by_token_hash(token_hash):
        return PasswordResetToken.query.filter_by(
            token_hash=token_hash
        ).first()

    @staticmethod
    def get_by_id(token_id):
        return db.session.get(
            PasswordResetToken,
            token_id
        )

    @staticmethod
    def get_by_token(token):
        return PasswordResetToken.query.filter_by(
            token=token
        ).first()

    @staticmethod
    def get_by_user_id(user_id):
        return PasswordResetToken.query.filter_by(
            user_id=user_id
        ).all()

    @staticmethod
    def create(reset_token):
        db.session.add(reset_token)
        db.session.flush()
        return reset_token

    @staticmethod
    def update():
        db.session.commit()

    @staticmethod
    def delete(reset_token):
        db.session.delete(reset_token)
        db.session.commit()

    @staticmethod
    def commit():
        db.session.commit()

    @staticmethod
    def mark_as_used(reset_token):
        reset_token.used_at = db.func.now()
        db.session.commit()

    @staticmethod
    def rollback():
        db.session.rollback()

        