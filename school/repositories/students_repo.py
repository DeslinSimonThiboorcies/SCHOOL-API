from school.extensison.db import db
from school.models.students import Student
from school.models.teacher import Teacher
class StudentsRepository:

    @staticmethod
    def create(student):
        db.session.add(student)
        db.session.commit()
        return student

    @staticmethod
    def read_mail(email):
        return Student.query.filter_by(
            email = email
        ).first()
    
    @staticmethod
    def read_teacher(email):
        return Teacher.query.filter_by(
            email = email
        ).first()
    
    @staticmethod
    def read_id(id):
        return db.session.get(
            Student,
            id
        )
       
    @staticmethod
    def get_all():
        return Student.query.all()
    
    @staticmethod
    def update_scool():
        db.session.commit()

    @staticmethod
    def remove_student(student):
        db.session.delete(student)
        db.session.commit()