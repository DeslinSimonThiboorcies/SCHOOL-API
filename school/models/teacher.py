from school.extensison.db import db
from datetime import datetime
from werkzeug.security import generate_password_hash , check_password_hash


class Teacher(db.Model):

    __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key = True)

    name = db.Column(
        db.String(50),
        nullable =False
    )
    role = db.Column(
        db.String(20),
        default = "TEACHER", 
        nullable =False,
    )
    department = db.Column(
        db.String(50),
        nullable =False,
    )
    email = db.Column(
        db.String(50),
        unique = True,
        nullable =False,
    )
    login_at = db.Column(
        db.DateTime,
        default = datetime.utcnow,
        nullable =False
    )
    update_at = db.Column(
        db.DateTime,
        default = datetime.utcnow,
        onupdate = datetime.utcnow,
        nullable =False
    )
    password = db.Column(
        db.String(225),
        nullable =False,
    )

    def set_teachers_password(self, password):
        self.password = generate_password_hash(password)

    def check_teachers_password(self, password):
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f"teachers<{self.name}>"