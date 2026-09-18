from school.extensison.db import db
from datetime import datetime, timezone


class Attendance(db.Model):
    __tablename__ = "attendance"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students_profiles.id"),
        nullable=False
    )

    class_id = db.Column(
        db.Integer,
        db.ForeignKey("class_model.id"),
        nullable=False
    )

    attendance_date = db.Column(
        db.Date,
        nullable=False
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="PRESENT"
    )

    marked_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    student_ref = db.relationship(
        "Student",
        backref="attendance_records"
    )

    class_ref = db.relationship(
        "ClassModel",
        backref="attendance_records"
    )

    def __repr__(self):
        return f"<Attendance student={self.student_id} date={self.attendance_date}>"