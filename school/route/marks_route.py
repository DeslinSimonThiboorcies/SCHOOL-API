from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from school.services.marks_service import MarksService
from school.Schema.marks_schema import (
    MarkCreateSchema,
    MarkUpdateSchema,
    MarkResponseSchema
)
from school.utils.role_decorator import role_require


marks_bp = Blueprint(
    "marks",
    __name__
)


create_schema = MarkCreateSchema()
update_schema = MarkUpdateSchema()
response_schema = MarkResponseSchema()
response_many_schema = MarkResponseSchema(many=True)

# CREATE MARKS
@marks_bp.route("/students/marks", methods=["POST"])
@jwt_required()
@role_require("PRINCIPAL", "TEACHER")
def create_marks():
    data = request.get_json()

    errors = create_schema.validate(data)

    if errors:
        return jsonify({
            "message": "Validation failed",
            "errors": errors
        }), 400

    try:
        marks = MarksService.create_mark(data)

        return jsonify({
            "message": "Marks created successfully",
            "data": response_schema.dump(marks)
        }), 201

    except ValueError as error:
        return jsonify({
            "message": str(error)
        }), 400

    except Exception as error:
        return jsonify({
            "message": "Failed to create marks",
            "error": str(error)
        }), 500

# GET ALL MARKS
@marks_bp.route("/students/marks", methods=["GET"])
@jwt_required()
@role_require("PRINCIPAL", "TEACHER")
def get_all_marks():
    try:
        marks_records = MarksService.get_all_marks()

        return jsonify({
            "message": "Marks fetched successfully",
            "data": response_many_schema.dump(marks_records)
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Failed to fetch marks",
            "error": str(error)
        }), 500

# GET MARKS BY ID
@marks_bp.route("/students/marks/<int:mark_id>", methods=["GET"])
@jwt_required()
@role_require("PRINCIPAL", "TEACHER")
def get_mark_by_id(mark_id):
    try:
        marks = MarksService.get_mark_by_id(mark_id)

        if not marks:
            return jsonify({
                "message": "Marks record not found"
            }), 404

        return jsonify({
            "message": "Marks fetched successfully",
            "data": response_schema.dump(marks)
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Failed to fetch marks",
            "error": str(error)
        }), 500

# GET MARKS BY STUDENT ID
@marks_bp.route("/students/marks/<int:student_id>", methods=["GET"])
@jwt_required()
@role_require("PRINCIPAL", "TEACHER")
def get_marks_by_student(student_id):
    try:
        marks_records = MarksService.get_by_student_id(student_id)

        return jsonify({
            "message": "Student marks fetched successfully",
            "data": response_many_schema.dump(marks_records)
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Failed to fetch student marks",
            "error": str(error)
        }), 500

# GET MARKS BY SUBJECT ID
@marks_bp.route("/subject/<int:subject_id>", methods=["GET"])
@jwt_required()
@role_require("PRINCIPAL", "TEACHER")
def get_marks_by_subject(subject_id):
    try:
        marks_records = MarksService.get_by_subject_id(subject_id)

        return jsonify({
            "message": "Subject marks fetched successfully",
            "data": response_many_schema.dump(marks_records)
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Failed to fetch subject marks",
            "error": str(error)
        }), 500
    
# GET MARKS BY EXAM NAME
@marks_bp.route("/students/marks/<string:exam_name>", methods=["GET"])
@jwt_required()
@role_require("PRINCIPAL", "TEACHER")
def get_marks_by_exam(exam_name):
    try:
        marks_records = MarksService.get_by_exam_name(exam_name)

        return jsonify({
            "message": "Exam marks fetched successfully",
            "data": response_many_schema.dump(marks_records)
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Failed to fetch exam marks",
            "error": str(error)
        }), 500

# UPDATE MARKS
@marks_bp.route("/update/students/marks<int:mark_id>", methods=["PUT"])
@jwt_required()
@role_require("PRINCIPAL", "TEACHER")
def update_marks(mark_id):
    data = request.get_json()

    errors = update_schema.validate(data)

    if errors:
        return jsonify({
            "message": "Validation failed",
            "errors": errors
        }), 400

    try:
        updated_marks = MarksService.update_mark(
            mark_id,
            data
        )

        if not updated_marks:
            return jsonify({
                "message": "Marks record not found"
            }), 404

        return jsonify({
            "message": "Marks updated successfully",
            "data": response_schema.dump(updated_marks)
        }), 200

    except ValueError as error:
        return jsonify({
            "message": str(error)
        }), 400

    except Exception as error:
        return jsonify({
            "message": "Failed to update marks",
            "error": str(error)
        }), 500

# DELETE MARKS
@marks_bp.route("/delete/students/marks<int:mark_id>", methods=["DELETE"])
@jwt_required()
@role_require("PRINCIPAL")
def delete_marks(mark_id):
    try:
        deleted = MarksService.delete_mark(mark_id)

        if not deleted:
            return jsonify({
                "message": "Marks record not found"
            }), 404

        return jsonify({
            "message": "Marks deleted successfully"
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Failed to delete marks",
            "error": str(error)
        }), 500