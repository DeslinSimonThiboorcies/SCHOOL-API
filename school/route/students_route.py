from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from school.services.students_services import StudentsServices

from school.Schema.student_schema import (
    StudentCreateSchema,
    StudentUpdateSchema,
    StudentResponseSchema
)


student_bp = Blueprint(
    "students",
    __name__
)


student_create_schema = StudentCreateSchema()
student_update_schema = StudentUpdateSchema()
student_response_schema = StudentResponseSchema()
student_response_many_schema = StudentResponseSchema(many=True)


@student_bp.route("/student/profile", methods=["POST"])
@jwt_required()
def create_student():
    claims = get_jwt()
    current_role = claims.get("role")

    if current_role not in ["PRINCIPAL", "TEACHER"]:
        return jsonify({
            "message": "Only principal or teacher can create students"
        }), 403

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request body is required"
        }), 400

    errors = student_create_schema.validate(data)

    if errors:
        return jsonify({
            "message": "Validation failed",
            "errors": errors
        }), 400

    try:
        student = StudentsServices.create_student(data)

        return jsonify({
            "message": "Student created successfully",
            "student": student_response_schema.dump(student)
        }), 201

    except ValueError as error:
        return jsonify({
            "message": str(error)
        }), 400

    except Exception as error:
        return jsonify({
            "message": "Something went wrong",
            "error": str(error)
        }), 500


@student_bp.route("view/profile", methods=["GET"])
@jwt_required()
def get_all_students():
    claims = get_jwt()
    current_role = claims.get("role")

    if current_role not in ["PRINCIPAL", "TEACHER"]:
        return jsonify({
            "message": "Only principal or teacher can view all students"
        }), 403

    try:
        students = StudentsServices.get_all_students()

        return jsonify({
            "message": "Students fetched successfully",
            "students": student_response_many_schema.dump(students)
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Something went wrong",
            "error": str(error)
        }), 500


@student_bp.route("/class/<int:class_id>", methods=["GET"])
@jwt_required()
def get_students_by_class(class_id):
    claims = get_jwt()
    current_role = claims.get("role")

    if current_role not in ["PRINCIPAL", "TEACHER"]:
        return jsonify({
            "message": "Only principal or teacher can view class students"
        }), 403

    try:
        students = StudentsServices.get_students_by_class_id(class_id)

        return jsonify({
            "message": "Students fetched successfully",
            "students": student_response_many_schema.dump(students)
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Something went wrong",
            "error": str(error)
        }), 500


@student_bp.route("/student/profile/<int:student_id>", methods=["GET"])
@jwt_required()
def get_student_by_id(student_id):
    current_user_id = int(get_jwt_identity())
    claims = get_jwt()
    current_role = claims.get("role")

    try:
        student = StudentsServices.get_student_by_id(student_id)

        if not student:
            return jsonify({
                "message": "Student not found"
            }), 404

        if current_role == "STUDENT":
            if student.user_id != current_user_id:
                return jsonify({
                    "message": "You can access only your own student profile"
                }), 403

        elif current_role not in ["PRINCIPAL", "TEACHER"]:
            return jsonify({
                "message": "Access denied"
            }), 403

        return jsonify({
            "message": "Student fetched successfully",
            "student": student_response_schema.dump(student)
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Something went wrong",
            "error": str(error)
        }), 500


@student_bp.route("/update/student/profile/<int:student_id>", methods=["PUT"])
@jwt_required()
def update_student(student_id):
    current_user_id = int(get_jwt_identity())
    claims = get_jwt()
    current_role = claims.get("role")

    try:
        existing_student = StudentsServices.get_student_by_id(student_id)

        if not existing_student:
            return jsonify({
                "message": "Student not found"
            }), 404

        if current_role == "STUDENT":
            if existing_student.user_id != current_user_id:
                return jsonify({
                    "message": "You can update only your own student profile"
                }), 403

        elif current_role not in ["PRINCIPAL", "TEACHER"]:
            return jsonify({
                "message": "Access denied"
            }), 403

        data = request.get_json()

        if not data:
            return jsonify({
                "message": "Request body is required"
            }), 400

        errors = student_update_schema.validate(data)

        if errors:
            return jsonify({
                "message": "Validation failed",
                "errors": errors
            }), 400

        student = StudentsServices.update_student(
            student_id,
            data
        )

        return jsonify({
            "message": "Student updated successfully",
            "student": student_response_schema.dump(student)
        }), 200

    except ValueError as error:
        return jsonify({
            "message": str(error)
        }), 400

    except Exception as error:
        return jsonify({
            "message": "Something went wrong",
            "error": str(error)
        }), 500


@student_bp.route("/delete/student/profile/<int:student_id>", methods=["DELETE"])
@jwt_required()
def delete_student(student_id):
    claims = get_jwt()
    current_role = claims.get("role")

    if current_role != "PRINCIPAL":
        return jsonify({
            "message": "Only principal can delete students"
        }), 403

    try:
        deleted = StudentsServices.delete_student(student_id)

        if not deleted:
            return jsonify({
                "message": "Student not found"
            }), 404

        return jsonify({
            "message": "Student deleted successfully"
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Something went wrong",
            "error": str(error)
        }), 500