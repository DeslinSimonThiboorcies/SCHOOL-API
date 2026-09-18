from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from school.services.subject_service import SubjectService

from school.Schema.subject_schema import (
    SubjectCreateSchema,
    SubjectUpdateSchema,
    SubjectResponseSchema
)

from school.utils.role_decorator import role_require


subject_bp = Blueprint(
    "subjects",
    __name__,
    url_prefix="/api/subjects"
)


subject_create_schema = SubjectCreateSchema()
subject_update_schema = SubjectUpdateSchema()
subject_response_schema = SubjectResponseSchema()
subject_response_many_schema = SubjectResponseSchema(many=True)


@subject_bp.route("/register/subject/", methods=["POST"])
@jwt_required()
@role_require("PRINCIPAL")
def create_subject():
    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request body is required"
        }), 400

    errors = subject_create_schema.validate(data)

    if errors:
        return jsonify({
            "message": "Validation failed",
            "errors": errors
        }), 400

    try:
        subject = SubjectService.create_subject(data)

        return jsonify({
            "message": "Subject created successfully",
            "subject": subject_response_schema.dump(subject)
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


@subject_bp.route("/view_all_subject/", methods=["GET"])
@jwt_required()
@role_require("PRINCIPAL", "TEACHER")
def get_all_subjects():
    try:
        subjects = SubjectService.get_all_subjects()

        return jsonify({
            "message": "Subjects fetched successfully",
            "subjects": subject_response_many_schema.dump(subjects)
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Something went wrong",
            "error": str(error)
        }), 500


@subject_bp.route("/view_subject/<int:subject_id>", methods=["GET"])
@jwt_required()
@role_require("PRINCIPAL", "TEACHER")
def get_subject_by_id(subject_id):
    try:
        subject = SubjectService.get_subject_by_id(subject_id)

        if not subject:
            return jsonify({
                "message": "Subject not found"
            }), 404

        return jsonify({
            "message": "Subject fetched successfully",
            "subject": subject_response_schema.dump(subject)
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Something went wrong",
            "error": str(error)
        }), 500


@subject_bp.route("/update/subject/<int:subject_id>", methods=["PUT"])
@jwt_required()
@role_require("PRINCIPAL")
def update_subject(subject_id):
    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request body is required"
        }), 400

    errors = subject_update_schema.validate(data)

    if errors:
        return jsonify({
            "message": "Validation failed",
            "errors": errors
        }), 400

    try:
        subject = SubjectService.update_subject(
            subject_id,
            data
        )

        if not subject:
            return jsonify({
                "message": "Subject not found"
            }), 404

        return jsonify({
            "message": "Subject updated successfully",
            "subject": subject_response_schema.dump(subject)
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


@subject_bp.route("/delet/subject/<int:subject_id>", methods=["DELETE"])
@jwt_required()
@role_require("PRINCIPAL")
def delete_subject(subject_id):
    try:
        deleted = SubjectService.delete_subject(subject_id)

        if not deleted:
            return jsonify({
                "message": "Subject not found"
            }), 404

        return jsonify({
            "message": "Subject deleted successfully"
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