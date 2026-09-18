from school.extensison.db import db
from datetime import datetime, timezone


class Fee(db.Model):
    __tablename__ = "fees"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students_profiles.id"),
        nullable=False
    )

    fee_type = db.Column(
        db.String(50),
        nullable=False
    )

    amount = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    due_date = db.Column(
        db.Date,
        nullable=False
    )

    payment_status = db.Column(
        db.String(20),
        nullable=False,
        default="PENDING"
    )

    paid_date = db.Column(
        db.Date,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    student_ref = db.relationship(
        "Student",
        backref="fees"
    )

    def __repr__(self):
        return f"<Fee student={self.student_id} type={self.fee_type}>"