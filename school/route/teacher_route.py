from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from school.services.teacher_service import TeacherServices

from school.Schema.teacher_schema import (
    TeacherCreateSchema,
    TeacherUpdateSchema,
    TeacherResponseSchema
)

from school.utils.role_decorator import role_require


teacher_bp = Blueprint(
    "teachers",
    __name__
)

teacher_create_schema = TeacherCreateSchema()
teacher_update_schema = TeacherUpdateSchema()
teacher_response_schema = TeacherResponseSchema()
teacher_response_many_schema = TeacherResponseSchema(many=True)


@teacher_bp.route("teachers/profile", methods=["POST"])
@jwt_required()
@role_require("PRINCIPAL")
def create_teacher():
    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request body is required"
        }), 400

    errors = teacher_create_schema.validate(data)

    if errors:
        return jsonify({
            "message": "Validation failed",
            "errors": errors
        }), 400

    try:
        teacher = TeacherServices.create_teacher(data)

        return jsonify({
            "message": "Teacher created successfully",
            "teacher": teacher_response_schema.dump(teacher)
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


@teacher_bp.route("teacher/profile", methods=["GET"])
@jwt_required()
@role_require("PRINCIPAL")
def get_all_teachers():
    try:
        teachers = TeacherServices.get_all_teachers()

        return jsonify({
            "message": "Teachers fetched successfully",
            "teachers": teacher_response_many_schema.dump(teachers)
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Something went wrong",
            "error": str(error)
        }), 500


@teacher_bp.route("/department/<string:department>", methods=["GET"])
@jwt_required()
@role_require("PRINCIPAL")
def get_teachers_by_department(department):
    try:
        teachers = TeacherServices.get_teachers_by_department(
            department
        )

        return jsonify({
            "message": "Teachers fetched successfully",
            "teachers": teacher_response_many_schema.dump(teachers)
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Something went wrong",
            "error": str(error)
        }), 500


@teacher_bp.route("teacher/<int:teacher_id>", methods=["GET"])
@jwt_required()
def get_teacher_by_id(teacher_id):
    current_user_id = int(get_jwt_identity())
    claims = get_jwt()
    current_role = claims.get("role")

    try:
        teacher = TeacherServices.get_teacher_by_id(teacher_id)

        if not teacher:
            return jsonify({
                "message": "Teacher not found"
            }), 404

        if current_role != "PRINCIPAL":
            if teacher.user_id != current_user_id:
                return jsonify({
                    "message": "You can access only your own teacher profile"
                }), 403

        return jsonify({
            "message": "Teacher fetched successfully",
            "teacher": teacher_response_schema.dump(teacher)
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Something went wrong",
            "error": str(error)
        }), 500


@teacher_bp.route("update/department/<int:teacher_id>", methods=["PUT"])
@jwt_required()
def update_teacher(teacher_id):
    current_user_id = int(get_jwt_identity())
    claims = get_jwt()
    current_role = claims.get("role")

    try:
        existing_teacher = TeacherServices.get_teacher_by_id(teacher_id)

        if not existing_teacher:
            return jsonify({
                "message": "Teacher not found"
            }), 404

        if current_role != "PRINCIPAL":
            if existing_teacher.user_id != current_user_id:
                return jsonify({
                    "message": "You can update only your own teacher profile"
                }), 403

        data = request.get_json()

        if not data:
            return jsonify({
                "message": "Request body is required"
            }), 400

        errors = teacher_update_schema.validate(data)

        if errors:
            return jsonify({
                "message": "Validation failed",
                "errors": errors
            }), 400

        teacher = TeacherServices.update_teacher(
            teacher_id,
            data
        )

        return jsonify({
            "message": "Teacher updated successfully",
            "teacher": teacher_response_schema.dump(teacher)
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


@teacher_bp.route("delete/department/<int:teacher_id>", methods=["DELETE"])
@jwt_required()
@role_require("PRINCIPAL")
def delete_teacher(teacher_id):
    try:
        deleted = TeacherServices.delete_teacher(teacher_id)

        if not deleted:
            return jsonify({
                "message": "Teacher not found"
            }), 404

        return jsonify({
            "message": "Teacher deleted successfully"
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Something went wrong",
            "error": str(error)
        }), 500