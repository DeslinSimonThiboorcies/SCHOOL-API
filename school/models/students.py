from school.extensison.db import db
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

class Student(db.Model):

    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key = True)

    name = db.Column(
        db.String(50), 
        nullable =False
    )

    role = db.Column(
        db.String(20),
        default = "STUDENT", 
        nullable =False,
    )

    email = db.Column(
        db.String(50),
        unique = True, 
        nullable =False
    )
    
    department = db.Column(
        db.String(20),
        default = "COMMERCES", 
        nullable =False, 
    )

    login_date = db.Column(
        db.DateTime,
        default = lambda : datetime.now(timezone.utc),
        nullable =False
    )
    update_at = db.Column(
        db.DateTime,
        default = lambda : datetime.now(timezone.utc),
        onupdate = lambda : datetime.now(timezone.utc),
        nullable =False
    )
    password = db.Column(
        db.String(225), 
        nullable =False,
    )

    def students_password(self, password):
        self.password = generate_password_hash(password)
    
    def verify_students_password(self, password):
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f"<students {self.name}>"