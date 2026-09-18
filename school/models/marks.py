from school.extensison.db import db
from datetime import datetime, timezone


class Mark(db.Model):
    __tablename__ = "marks"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students_profiles.id"),
        nullable=False
    )

    subject_id = db.Column(
        db.Integer,
        db.ForeignKey("subjects.id"),
        nullable=False
    )

    exam_name = db.Column(
        db.String(100),
        nullable=False
    )

    marks_obtained = db.Column(
        db.Float,
        nullable=False
    )

    maximum_marks = db.Column(
        db.Float,
        nullable=False
    )

    exam_date = db.Column(
        db.Date,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    student_ref = db.relationship(
        "Student",
        backref="marks"
    )

    subject_ref = db.relationship(
        "Subject",
        backref="marks"
    )

    def __repr__(self):
        return f"<Mark student={self.student_id} subject={self.subject_id}>"