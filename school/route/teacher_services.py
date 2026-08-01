from flask import Blueprint, request, jsonify
from school.services.teacher_service import TeacherServices
from flask_jwt_extended import get_jwt_identity, jwt_required
from school.utils.teacher_dec import principle

teach_bp = Blueprint(
    "teachers",
    __name__
)

@teach_bp.route("/register_teachers", methods =["POST"])
def register():

    data = request.get_json()

    TeacherServices.register_teacher(data)
    return jsonify({
        "MESSAGE" : "TEACHER CREATE SUCCESSFULLY"
    }), 201

@teach_bp.route("/login_teachers", methods =["POST"])
def login_teacher():

    data = request.get_json()
    teacher = TeacherServices.login_teacher(data)

    if not teacher:
        return jsonify({
            "MESSAGE" : "USER NOT FOUND!"
        }), 404
    return jsonify({
        "MESSAGE" : teacher
    }), 200

@teach_bp.route("/view_all_teachers", methods =["GET"])
@jwt_required()
@principle
def view_all():

    teacher = TeacherServices.teachers_profiles()

    if not teacher:
        return jsonify({
            "MESSAGE" : "USER NOT FOUND!"
        }), 404
    
    responds = []

    for teachers in teacher:
        responds.append({
            "name" : teachers.name,
            "role" : teachers.role,
            "department" : teachers.department,
            "email" : teachers.email,
            "login_at" :teachers.login_at,
            "update_at" : teachers.update_at
        })

    return jsonify({
        "MESSAGE" : responds
    }), 200

@teach_bp.route("/single_profile/<int:id>", methods =["GET"])
@jwt_required()
def my_profile(id):

    teachers = int(get_jwt_identity())
    teacher = TeacherServices.teacher_profile(teachers)

    if teacher.role != "PRINCIPAL" and teacher.id != id:
        return jsonify({
            "MESSAGE" : "ACCESS DENIED!"
        })
    
    if not teacher:
        return jsonify({
            "MESSAGE" : "USER NOT FOUND!"
        }),404
    
    responds = {
        "name" : teacher.name,
        "role" : teacher.role,
        "department" : teacher.department,
        "email" : teacher.email,
        "login_at" :teacher.login_at,
        "update_at" : teacher.update_at
    }
    return jsonify({
        "MESSAGE" : responds
    }), 200

@teach_bp.route("/update_teacher/<int:id>", methods =["PUT"])
@jwt_required()
def update_teach(id):

    teacher = int(get_jwt_identity())
    schools = TeacherServices.teacher_profile(teacher)

    if schools.role != "PRINCIPAL" and schools.id != id:
        return jsonify({
            "MESSAGE" : "ACCESS DENIED!"
        }), 403
       
    teachers = TeacherServices.teacher_profile(id)
    data = request.get_json()

    if not teachers:
        return jsonify({
            "MESSAGE" : "USER NOT FOUND!"
        }), 404
    
    TeacherServices.update(teachers, data)
    return jsonify({
        "MESSAGE" : "TEACHER UPDATE SUCCESS"
    }), 200

@teach_bp.route("/delete_teacher/<int:id>", methods =["DELETE"])
@jwt_required()
def delete_teach(id):

    teacher = int(get_jwt_identity())
    teachers = TeacherServices.teacher_profile(teacher)

    if teachers.role != "PRINCIPAL" and teachers.id != id:
        return jsonify({
            "MESSAGE" : "ACCESS DENIED!"
        }), 403
    
    school_principle = TeacherServices.teacher_profile(id)

    if not school_principle:
        return jsonify({
            "MESSAGE" : "USER NOT FOUND!"
        }), 404
    
    TeacherServices.delete(school_principle)
    return jsonify({
        "MESSAGE" : "TEACHER SUCCESSFULLY DELETE!"
    }),200