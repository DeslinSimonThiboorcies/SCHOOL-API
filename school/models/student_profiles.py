from school.extensison.db import db
from datetime import datetime, timezone

class Student(db.Model):

    __tablename__ = "students_profiles"

    id = db.Column(db.Integer, primary_key = True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable = False
    )

    admission_number = db.Column(
        db.String(20),
        unique = True,
        nullable =False,
    )

    joining_date = db.Column(
        db.DateTime,
        default = lambda : datetime.now(timezone.utc),
        nullable =False
    )

    class_id = db.Column(
        db.Integer,
        db.ForeignKey("class_model.id"),
        nullable=False
    )
    
    parent_name = db.Column(
        db.String(20),
        nullable =False, 
    )

    parent_phone = db.Column(
        db.String(15),
        nullable =False, 
    )