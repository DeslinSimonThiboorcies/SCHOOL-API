from school.repositories.teacher_repo import TeacherRepository
from school.models.teacher import Teacher
from flask_jwt_extended import create_access_token

class  TeacherServices:

    try:

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
        
    except Exception as e:
        raise ValueError(
            f"{e}"
        )