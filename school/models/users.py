from school.extensison.db import db
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)

    full_name = db.Column(
        db.String(50), 
        nullable =False
    )

    email = db.Column(
        db.String(50),
        unique = True, 
        nullable =False
    )

    phone_number = db.Column(
        db.String(15),
        unique = True
    )

    date_of_birth = db.Column(
        db.Date,
        nullable = False
    )

    role = db.Column(
        db.String(20),
        default = "STUDENT", 
        nullable =False,
    )

    password = db.Column(
         db.String(225), 
        nullable =False,
    )

    login_date = db.Column(
        db.DateTime,
        default = lambda : datetime.now(timezone.utc),
        nullable =False
    )

    def users_password(self, password):
        self.password = generate_password_hash(password)
    
    def verify_users_password(self, password):
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f"<users {self.full_name}>"