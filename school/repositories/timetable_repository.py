from school.extensison.db import db
from school.models.timetable import Timetable


class TimetableRepository:

    @staticmethod
    def get_by_id(timetable_id):
        return db.session.get(Timetable, timetable_id)

    @staticmethod
    def get_all():
        return Timetable.query.all()

    @staticmethod
    def get_by_class_id(class_id):
        return Timetable.query.filter_by(
            class_id=class_id
        ).all()

    @staticmethod
    def get_by_teacher_id(teacher_id):
        return Timetable.query.filter_by(
            teacher_id=teacher_id
        ).all()

    @staticmethod
    def get_by_subject_id(subject_id):
        return Timetable.query.filter_by(
            subject_id=subject_id
        ).all()

    @staticmethod
    def get_by_class_and_day(class_id, day_of_week):
        return Timetable.query.filter_by(
            class_id=class_id,
            day_of_week=day_of_week
        ).all()

    @staticmethod
    def create(timetable):
        db.session.add(timetable)
        db.session.flush()
        return timetable

    @staticmethod
    def update():
        db.session.commit()

    @staticmethod
    def delete(timetable):
        db.session.delete(timetable)
        db.session.commit()

    @staticmethod
    def commit():
        db.session.commit()

    @staticmethod
    def rollback():
        db.session.rollback()