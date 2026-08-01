from school.models.teacher import Teacher
from school.extensison.db import db

class TeacherRepository:

    @staticmethod
    def create_teacher(teachers):
        db.session.add(teachers)
        db.session.commit()
        return teachers
    
    @staticmethod
    def teacher_mail(email):
        return Teacher.query.filter_by(
            email = email
        ).first()
    
    @staticmethod
    def view_all_teachers():
        return Teacher.query.all()
    
    @staticmethod
    def view_teacher(id):
        return db.session.get(
            Teacher,
            id
        )        
    @staticmethod
    def delete_teacher(teacher):
        db.session.delete(teacher)
        db.session.commit()
    
    @staticmethod
    def update_teacher():
        db.session.commit()

    