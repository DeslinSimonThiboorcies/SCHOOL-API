from school.extensison.db import db
from school.models.attendance import Attendance


class AttendanceRepository:

    @staticmethod
    def get_by_id(attendance_id):
        return db.session.get(Attendance, attendance_id)

    @staticmethod
    def get_all():
        return Attendance.query.all()

    @staticmethod
    def get_by_student_id(student_id):
        return Attendance.query.filter_by(
            student_id=student_id
        ).all()

    @staticmethod
    def get_by_class_id(class_id):
        return Attendance.query.filter_by(
            class_id=class_id
        ).all()

    @staticmethod
    def get_by_student_and_date(student_id, attendance_date):
        return Attendance.query.filter_by(
            student_id=student_id,
            attendance_date=attendance_date
        ).first()

    @staticmethod
    def create(attendance):
        db.session.add(attendance)
        db.session.flush()
        return attendance

    @staticmethod
    def update():
        db.session.commit()

    @staticmethod
    def delete(attendance):
        db.session.delete(attendance)
        db.session.commit()

    @staticmethod
    def commit():
        db.session.commit()

    @staticmethod
    def rollback():
        db.session.rollback()