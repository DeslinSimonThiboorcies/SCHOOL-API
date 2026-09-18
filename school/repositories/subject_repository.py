from school.extensison.db import db
from school.models.subject import Subject


class SubjectRepository:

    @staticmethod
    def get_by_id(subject_id):
        return db.session.get(Subject, subject_id)

    @staticmethod
    def get_all():
        return Subject.query.all()

    @staticmethod
    def get_by_name(subject_name):
        return Subject.query.filter_by(
            subject_name=subject_name
        ).first()

    @staticmethod
    def get_by_code(subject_code):
        return Subject.query.filter_by(
            subject_code=subject_code
        ).first()

    @staticmethod
    def create(subject):
        db.session.add(subject)
        db.session.flush()
        return subject

    @staticmethod
    def update():
        db.session.commit()

    @staticmethod
    def delete(subject):
        db.session.delete(subject)
        db.session.commit()

    @staticmethod
    def commit():
        db.session.commit()

    @staticmethod
    def rollback():
        db.session.rollback()