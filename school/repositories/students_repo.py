from school.extensison.db import db
from school.models.student_profiles import Student
from school.models.teacher_profile import Teacher
from school.models.users import User


class StudentRepository:

    @staticmethod
    def get_by_id(student_id):
        return db.session.get(Student, student_id)

    @staticmethod
    def get_by_user_id(user_id):
        return Student.query.filter_by(
            user_id=user_id
        ).first()

    @staticmethod
    def get_by_admission_number(admission_number):
        return Student.query.filter_by(
            admission_number=admission_number
        ).first()

    @staticmethod
    def get_by_class_id(class_id):
        return Student.query.filter_by(
            class_id=class_id
        ).all()

    @staticmethod
    def read_mail(email):
        return Student.query.join(User).filter(User.email == email).first()

    @staticmethod
    def read_teacher(email):
        return Teacher.query.join(User).filter(User.email == email).first()

    @staticmethod
    def read_id(student_id):
        return StudentRepository.get_by_id(student_id)

    @staticmethod
    def update_scool():
        StudentRepository.update()

    @staticmethod
    def remove_student(student):
        StudentRepository.delete(student)

    @staticmethod
    def get_all():
        return Student.query.all()

    @staticmethod
    def create(student):
        db.session.add(student)
        db.session.flush()
        return student

    @staticmethod
    def update():
        db.session.commit()

    @staticmethod
    def delete(student):
        db.session.delete(student)
        db.session.commit()

    @staticmethod
    def commit():
        db.session.commit()

    @staticmethod
    def rollback():
        db.session.rollback()


StudentsRepository = StudentRepository