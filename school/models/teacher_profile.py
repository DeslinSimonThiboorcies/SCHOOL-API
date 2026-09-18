from school.extensison.db import db
from datetime import datetime, timezone

class Teacher(db.Model):

    __tablename__ = "teacher_profile"

    id = db.Column(db.Integer, primary_key = True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable = False
    )
    employee_number = db.Column(
        db.String(20),
        nullable =False,
        unique = True
    )
    department = db.Column(
        db.String(50),
        nullable =False,
    )
    qualification = db.Column(
        db.String(50),
        nullable =False,
    )
    joining_date = db.Column(
        db.DateTime,
        default = lambda : datetime.now(timezone.utc),
        nullable =False
    )