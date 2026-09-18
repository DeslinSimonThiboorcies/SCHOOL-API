from school.extensison.db import db
from datetime import datetime, timezone


class ClassModel(db.Model):

    __tablename__ = "class_model"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    class_name = db.Column(
        db.String(50),
        nullable=False
    )

    section = db.Column(
        db.String(10),
        nullable=False
    )

    academic_year = db.Column(
        db.String(20),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    def __repr__(self):
        return f"<ClassModel {self.class_name} - {self.section}>"