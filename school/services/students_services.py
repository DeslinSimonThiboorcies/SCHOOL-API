from school.repositories.students_repo import StudentsRepository
from school.models.student_profiles import Student
from school.models.users import User
from school.extensison.db import db
from flask_jwt_extended import create_access_token

class StudentsServices:

    @staticmethod
    def create_student(data):
        user = db.session.get(User, data["user_id"])
        if not user:
            raise ValueError("User not found")

        if StudentsRepository.get_by_user_id(user.id):
            raise ValueError("Student profile already exists")

        student = Student(
            user_id=user.id,
            admission_number=data["admission_number"],
            joining_date=data.get("joining_date"),
            class_id=data["class_id"],
            parent_name=data["parent_name"],
            parent_phone=data["parent_phone"],
        )
        StudentsRepository.create(student)
        StudentsRepository.commit()
        return student

    @staticmethod
    def get_all_students():
        return StudentsRepository.get_all()

    @staticmethod
    def get_students_by_class_id(class_id):
        return StudentsRepository.get_by_class_id(class_id)

    @staticmethod
    def get_student_by_id(student_id):
        return StudentsRepository.get_by_id(student_id)

    @staticmethod
    def update_student(student_id, data):
        student = StudentsRepository.get_by_id(student_id)
        if not student:
            return None

        for field in ("admission_number", "class_id", "parent_name", "parent_phone"):
            if field in data:
                setattr(student, field, data[field])
        StudentsRepository.commit()
        return student

    @staticmethod
    def delete_student(student_id):
        student = StudentsRepository.get_by_id(student_id)
        if not student:
            return None
        StudentsRepository.delete(student)
        return student

    @staticmethod
    def students_register(data):

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        verify_teacher = StudentsRepository.read_teacher(email)
        if verify_teacher:
            raise ValueError(
                "THIS EMAIL ALREADY REGISTER AT A TEACHERS"
            )
        
        student_verify = StudentsRepository.read_mail(email)

        if student_verify:
            raise ValueError(
                "THIS EMAIL ALREADY REGISTER AT A STUDENT"
            )
        
        students = Student(
            name = name,
            email = email
        )

        students.students_password(password)
        StudentsRepository.create(students)
        return students


    @staticmethod
    def login(data):

        email = data.get("email")
        password = data.get("password")

        verify_student = StudentsRepository.read_mail(email)

        if not verify_student:
            raise ValueError(
                "STUDENT NOT FOUND!"
            )
        
        if not verify_student.verify_students_password(password):
            raise ValueError(
                "INVALID PASSWORD!"
            )
        
        access = create_access_token(
            identity=str(verify_student.id)
        )
        return access
    
    @staticmethod
    def all_profile():

        return StudentsRepository.get_all()
    
    @staticmethod
    def profile(students_id):

        return StudentsRepository.read_id(students_id)
    
    @staticmethod
    def update(students, data):

        students.name = data.get("name", students.name)
        students.email = data.get("email", students.email)

        StudentsRepository.update_scool()
        return students

    @staticmethod
    def delete(students):

        StudentsRepository.remove_student(students)
        return True