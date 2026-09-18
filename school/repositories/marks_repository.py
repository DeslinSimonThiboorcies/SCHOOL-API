from school.extensison.db import db
from school.models.marks import Mark


class MarksRepository:

    @staticmethod
    def get_by_id(mark_id):
        return db.session.get(Mark, mark_id)

    @staticmethod
    def get_all():
        return Mark.query.all()

    @staticmethod
    def get_by_student_id(student_id):
        return Mark.query.filter_by(
            student_id=student_id
        ).all()

    @staticmethod
    def get_by_subject_id(subject_id):
        return Mark.query.filter_by(
            subject_id=subject_id
        ).all()

    @staticmethod
    def get_by_student_and_subject(student_id, subject_id):
        return Mark.query.filter_by(
            student_id=student_id,
            subject_id=subject_id
        ).all()

    @staticmethod
    def get_by_exam_name(exam_name):
        return Mark.query.filter_by(
            exam_name=exam_name
        ).all()

    @staticmethod
    def create(mark):
        db.session.add(mark)
        db.session.flush()
        return mark

    @staticmethod
    def update():
        db.session.commit()

    @staticmethod
    def delete(mark):
        db.session.delete(mark)
        db.session.commit()

    @staticmethod
    def commit():
        db.session.commit()

    @staticmethod
    def rollback():
        db.session.rollback()