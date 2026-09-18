from school.repositories.teacher_repo import TeacherRepository
from school.models.teacher_profile import Teacher
from school.models.users import User
from school.extensison.db import db
from flask_jwt_extended import create_access_token

class  TeacherServices:

    @staticmethod
    def create_teacher(data):
        user = db.session.get(User, data["user_id"])
        if not user:
            raise ValueError("User not found")

        if TeacherRepository.get_by_user_id(user.id):
            raise ValueError("Teacher profile already exists")

        teacher = Teacher(
            user_id=user.id,
            employee_number=data["employee_number"],
            department=data["department"],
            qualification=data["qualification"],
        )
        TeacherRepository.create(teacher)
        TeacherRepository.commit()
        return teacher

    @staticmethod
    def get_all_teachers():
        return TeacherRepository.get_all()

    @staticmethod
    def get_teachers_by_department(department):
        return TeacherRepository.get_by_department(department)

    @staticmethod
    def get_teacher_by_id(teacher_id):
        return TeacherRepository.get_by_id(teacher_id)

    @staticmethod
    def update_teacher(teacher_id, data):
        teacher = TeacherRepository.get_by_id(teacher_id)
        if not teacher:
            return None

        for field in ("employee_number", "department", "qualification"):
            if field in data:
                setattr(teacher, field, data[field])
        TeacherRepository.commit()
        return teacher

    @staticmethod
    def delete_teacher(teacher_id):
        teacher = TeacherRepository.get_by_id(teacher_id)
        if not teacher:
            return None
        TeacherRepository.delete(teacher)
        return teacher

    @staticmethod
    def register_teacher(data):

        name = data.get("name")
        department = data.get("department")
        email = data.get("email")
        password = data.get("password")

        verify_teachers = TeacherRepository.teacher_mail(email)
        if verify_teachers:
            raise ValueError(
                "USER ALREADY EXIST!"
            )   
            
        teachers = Teacher(
            name = name,
            department = department,
            email = email
        )
        
        teachers.set_teachers_password(password)
        TeacherRepository.create_teacher(teachers)
        return teachers

    @staticmethod
    def login_teacher(data):

        email = data.get("email")
        password = data.get("password")

        verify_teacher = TeacherRepository.teacher_mail(email)
        if not verify_teacher:
            raise ValueError(
                "INVALID USER"
            )
        if not verify_teacher.check_teachers_password(password):
            raise ValueError(
                "INVALID PASSWORD OR EMAIL"
            )
        
        token = create_access_token(
            identity=str(verify_teacher.id)
        )

        return token
    
    @staticmethod
    def teachers_profiles():
    
        return TeacherRepository.view_all_teachers()
    
    @staticmethod
    def teacher_profile(teacher_id):

        return TeacherRepository.view_teacher(teacher_id)
    
    @staticmethod
    def update(teacher, data):

        teacher.name = data.get("name", teacher.name)
        teacher.department = data.get("department", teacher.department)
        teacher.email = data.get("email", teacher.email)

        TeacherRepository.update_teacher()
        return teacher
    
    @staticmethod
    def delete(teacher):

        TeacherRepository.delete_teacher(teacher)
        return True