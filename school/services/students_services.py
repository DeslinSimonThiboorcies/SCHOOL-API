from school.repositories.students_repo import StudentsRepository
from school.models.students import Student
from flask_jwt_extended import create_access_token

class StudentsServices:

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