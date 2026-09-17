from datetime import datetime, timezone
from school.extensison.db import db

class PasswordResetToken(db.Model):

    __tablename__ = "password_reset"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    account_type = db.Column(
        db.String(20),
        nullable=False
    )

    account_id = db.Column(
        db.Integer,
        nullable=False
    )

    token_hash = db.Column(
        db.String(255),
        nullable=False
    )

    expires_at = db.Column(
        db.DateTime,
        nullable=False
    )

    used_at = db.Column(
        db.DateTime,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        nullable=False
    )