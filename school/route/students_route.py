from flask import Blueprint, request, jsonify
from school.services.students_services import StudentsServices
from school.utils.students_dec import school_principl
from flask_jwt_extended import jwt_required, get_jwt_identity

student_bp = Blueprint(
    "auth",
    __name__
)

@student_bp.route("/register", methods =["POST"])
def register():

    data = request.get_json()
    StudentsServices.students_register(data)

    return jsonify({
        "Message" : "Data Create Successfully"
    })

@student_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()
    student = StudentsServices.login(data)

    if not student:
        return jsonify({
            "Message" : "Data not found!"
        }), 404
    
    return jsonify({
        "TOKEN" : student
    }), 200

@student_bp.route("/all_profile", methods = ["GET"])
@jwt_required()
@school_principl
def all_students():

    student = StudentsServices.all_profile()

    if not student:
        return jsonify({
            "MESSAGE" : "STUDENTS NOT FOUND!"
        }), 404
    
    responds = []

    for students in student:
        responds.append({
            "id" : students.id,
            "name" : students.name,
            "role" : students.role,
            "email" : students.email,
            "department" : students.department,
            "login_date" : students.login_date
        })
    return jsonify({
        "MESSAGE" : responds
    }), 200

@student_bp.route("/my_profile/<int:id>", methods = ["GET"])
@jwt_required()
def my_profile(id):

    students = int(get_jwt_identity())
    student = StudentsServices.profile(students)

    if not student:
        return jsonify({
            "MESSAGE" : "USER NOT FOUND!"
        }), 404
    
    if student.role != ["PRINCIPAL" or "TEACHER"] and\
        student.id != id:
        return jsonify({
            "NOTE" : "ACCESS DENIED"
        }), 403
   
    responds = {
        "id" : student.id,
        "name" : student.name,
        "role" : student.role,
        "email" : student.email,
        "department" : student.department,
        "login_date" : student.login_date
        }
    
    return jsonify({
        "MESSAGE" : responds
    }), 200

@student_bp.route("/update/<int:id>", methods = ["PUT"])
@jwt_required()
def update(id):

    student = int(get_jwt_identity())
    school = StudentsServices.profile(student)
    
    if school.role != ["PRINCIPAL" or "TEACHER"] and\
        school.id != id:
        return jsonify({
            "NOTE" : "ACCESS DENIED"
        }), 403
    
    students = StudentsServices.profile(id)

    if not students:
        return jsonify({
            "MESSAGE" : "USER NOT FOUND!"
        }), 404
    
    data = request.get_json()
    StudentsServices.update(school, data)
    return jsonify({
        "MESSAGE" : "STUDENT UPDATE SUCCESSFUL"
    }), 200

@student_bp.route("/delete/<int:id>", methods = ["DELETE"])
@jwt_required()
def remove(id):

    school = int(get_jwt_identity())
    students = StudentsServices.profile(school)

    if students.role != ["PRINCIPAL" or "TEACHER"] and\
        students.id != id:
        return jsonify({
            "NOTE" : "ACCESS DENIED"
        }), 403
    
    student = StudentsServices.profile(id)

    if not student:
        return jsonify({
            "MESSAGE" : "USER NOT FOUND!"
        }), 404
    
    StudentsServices.delete(student)
    return jsonify({
        "MESSAGE" : "SUCCESSFULLY DELETED!"
    }), 200