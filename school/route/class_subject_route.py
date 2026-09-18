from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from school.services.class_subject_service import ClassSubjectService
from school.Schema.class_subject_schema import (
    ClassSubjectCreateSchema,
    ClassSubjectUpdateSchema,
    ClassSubjectResponseSchema
)
from school.utils.role_decorator import role_require


class_subject_bp = Blueprint(
    "class_subjects",
    __name__
)


create_schema = ClassSubjectCreateSchema()
update_schema = ClassSubjectUpdateSchema()
response_schema = ClassSubjectResponseSchema()
response_many_schema = ClassSubjectResponseSchema(many=True)


# CREATE CLASS-SUBJECT ASSIGNMENT

@class_subject_bp.route("/class/subjects", methods=["POST"])
@jwt_required()
@role_require("PRINCIPAL")
def create_class_subject():
    data = request.get_json()

    errors = create_schema.validate(data)

    if errors:
        return jsonify({
            "message": "Validation failed",
            "errors": errors
        }), 400

    try:
        class_subject = ClassSubjectService.create_class_subject(data)

        return jsonify({
            "message": "Subject assigned to class successfully",
            "data": response_schema.dump(class_subject)
        }), 201

    except ValueError as error:
        return jsonify({
            "message": str(error)
        }), 400

    except Exception as error:
        return jsonify({
            "message": "Failed to assign subject to class",
            "error": str(error)
        }), 500

# GET ALL CLASS-SUBJECT ASSIGNMENTS

@class_subject_bp.route("/class/subject", methods=["GET"])
@jwt_required()
@role_require("PRINCIPAL", "TEACHER")
def get_all_class_subjects():
    try:
        assignments = ClassSubjectService.get_all_class_subjects()

        return jsonify({
            "message": "Class-subject assignments fetched successfully",
            "data": response_many_schema.dump(assignments)
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Failed to fetch class-subject assignments",
            "error": str(error)
        }), 500

# GET ASSIGNMENT BY ID

@class_subject_bp.route("/class/subject/<int:class_subject_id>", methods=["GET"])
@jwt_required()
@role_require("PRINCIPAL", "TEACHER")
def get_class_subject_by_id(class_subject_id):
    try:
        class_subject = ClassSubjectService.get_class_subject_by_id(
            class_subject_id
        )

        if not class_subject:
            return jsonify({
                "message": "Class-subject assignment not found"
            }), 404

        return jsonify({
            "message": "Class-subject assignment fetched successfully",
            "data": response_schema.dump(class_subject)
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Failed to fetch assignment",
            "error": str(error)
        }), 500

# GET ASSIGNMENTS BY CLASS ID

@class_subject_bp.route("/class/subject/<int:class_id>", methods=["GET"])
@jwt_required()
@role_require("PRINCIPAL", "TEACHER")
def get_assignments_by_class(class_id):
    try:
        assignments = ClassSubjectService.get_by_class_id(class_id)

        return jsonify({
            "message": "Assignments for class fetched successfully",
            "data": response_many_schema.dump(assignments)
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Failed to fetch class assignments",
            "error": str(error)
        }), 500

# GET ASSIGNMENTS BY SUBJECT ID
@class_subject_bp.route("/class/subject/<int:subject_id>", methods=["GET"])
@jwt_required()
@role_require("PRINCIPAL", "TEACHER")
def get_assignments_by_subject(subject_id):
    try:
        assignments = ClassSubjectService.get_by_subject_id(subject_id)

        return jsonify({
            "message": "Assignments for subject fetched successfully",
            "data": response_many_schema.dump(assignments)
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Failed to fetch subject assignments",
            "error": str(error)
        }), 500


# GET ASSIGNMENTS BY TEACHER ID
@class_subject_bp.route("/class/teacher/subject/<int:teacher_id>", methods=["GET"])
@jwt_required()
@role_require("PRINCIPAL", "TEACHER")
def get_assignments_by_teacher(teacher_id):
    try:
        assignments = ClassSubjectService.get_by_teacher_id(teacher_id)

        return jsonify({
            "message": "Assignments for teacher fetched successfully",
            "data": response_many_schema.dump(assignments)
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Failed to fetch teacher assignments",
            "error": str(error)
        }), 500

# UPDATE CLASS-SUBJECT ASSIGNMENT
@class_subject_bp.route("/class/subject/update/<int:class_subject_id>", methods=["PUT"])
@jwt_required()
@role_require("PRINCIPAL")
def update_class_subject(class_subject_id):
    data = request.get_json()

    errors = update_schema.validate(data)

    if errors:
        return jsonify({
            "message": "Validation failed",
            "errors": errors
        }), 400

    try:
        updated_assignment = ClassSubjectService.update_class_subject(
            class_subject_id,
            data
        )

        if not updated_assignment:
            return jsonify({
                "message": "Class-subject assignment not found"
            }), 404

        return jsonify({
            "message": "Class-subject assignment updated successfully",
            "data": response_schema.dump(updated_assignment)
        }), 200

    except ValueError as error:
        return jsonify({
            "message": str(error)
        }), 400

    except Exception as error:
        return jsonify({
            "message": "Failed to update assignment",
            "error": str(error)
        }), 500

# DELETE CLASS-SUBJECT ASSIGNMENT
@class_subject_bp.route("/class/subject/delete/<int:class_subject_id>", methods=["DELETE"])
@jwt_required()
@role_require("PRINCIPAL")
def delete_class_subject(class_subject_id):
    try:
        deleted = ClassSubjectService.delete_class_subject(
            class_subject_id
        )

        if not deleted:
            return jsonify({
                "message": "Class-subject assignment not found"
            }), 404

        return jsonify({
            "message": "Class-subject assignment deleted successfully"
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Failed to delete assignment",
            "error": str(error)
        }), 500