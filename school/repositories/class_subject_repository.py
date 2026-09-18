from school.extensison.db import db
from school.models.class_subject import ClassSubject


class ClassSubjectRepository:

    @staticmethod
    def get_by_id(class_subject_id):
        return db.session.get(ClassSubject, class_subject_id)

    @staticmethod
    def get_all():
        return ClassSubject.query.all()

    @staticmethod
    def get_by_class_id(class_id):
        return ClassSubject.query.filter_by(
            class_id=class_id
        ).all()

    @staticmethod
    def get_by_subject_id(subject_id):
        return ClassSubject.query.filter_by(
            subject_id=subject_id
        ).all()

    @staticmethod
    def get_by_class_and_subject(class_id, subject_id):
        return ClassSubject.query.filter_by(
            class_id=class_id,
            subject_id=subject_id
        ).first()

    @staticmethod
    def create(class_subject):
        db.session.add(class_subject)
        db.session.flush()
        return class_subject

    @staticmethod
    def update():
        db.session.commit()

    @staticmethod
    def delete(class_subject):
        db.session.delete(class_subject)
        db.session.commit()

    @staticmethod
    def commit():
        db.session.commit()

    @staticmethod
    def rollback():
        db.session.rollback()