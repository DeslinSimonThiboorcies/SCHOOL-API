from school.extensison.db import db
from school.models.teacher_profile import Teacher
from school.models.users import User


class TeacherRepository:

    @staticmethod
    def get_by_id(teacher_id):
        return db.session.get(Teacher, teacher_id)

    @staticmethod
    def get_by_user_id(user_id):
        return Teacher.query.filter_by(
            user_id=user_id
        ).first()

    @staticmethod
    def get_by_employee_number(employee_number):
        return Teacher.query.filter_by(
            employee_number=employee_number
        ).first()

    @staticmethod
    def get_by_department(department):
        return Teacher.query.filter_by(
            department=department
        ).all()

    @staticmethod
    def teacher_mail(email):
        return Teacher.query.join(User).filter(User.email == email).first()

    @staticmethod
    def view_teacher(teacher_id):
        return TeacherRepository.get_by_id(teacher_id)

    @staticmethod
    def get_all():
        return Teacher.query.all()

    @staticmethod
    def create(teacher):
        db.session.add(teacher)
        db.session.flush()
        return teacher

    @staticmethod
    def update():
        db.session.commit()

    @staticmethod
    def delete(teacher):
        db.session.delete(teacher)
        db.session.commit()

    @staticmethod
    def commit():
        db.session.commit()

    @staticmethod
    def rollback():
        db.session.rollback()