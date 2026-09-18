from school.extensison.db import db
from school.models.users import User


class UserRepository:

    @staticmethod
    def get_by_id(user_id):
        return db.session.get(User, user_id)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(
            email=email
        ).first()

    @staticmethod
    def get_by_phone_number(phone_number):
        return User.query.filter_by(
            phone_number=phone_number
        ).first()

    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def create(user):
        db.session.add(user)
        db.session.flush()
        return user

    @staticmethod
    def update():
        db.session.commit()

    @staticmethod
    def delete(user):
        db.session.delete(user)
        db.session.commit()

    @staticmethod
    def commit():
        db.session.commit()

    @staticmethod
    def rollback():
        db.session.rollback()