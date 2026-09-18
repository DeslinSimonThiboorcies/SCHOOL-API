from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from school.services.timetable_service import TimetableService
from school.Schema.timetable_schema import (
    TimetableCreateSchema,
    TimetableUpdateSchema,
    TimetableResponseSchema
)
from school.utils.role_decorator import role_require


timetable_bp = Blueprint(
    "timetable",
    __name__
)


create_schema = TimetableCreateSchema()
update_schema = TimetableUpdateSchema()
response_schema = TimetableResponseSchema()
response_many_schema = TimetableResponseSchema(many=True)

# CREATE TIMETABLE
@timetable_bp.route("/timetable", methods=["POST"])
@jwt_required()
@role_require("PRINCIPAL")
def create_timetable():
    data = request.get_json()

    errors = create_schema.validate(data)

    if errors:
        return jsonify({
            "message": "Validation failed",
            "errors": errors
        }), 400

    try:
        timetable = TimetableService.create_timetable(data)

        return jsonify({
            "message": "Timetable created successfully",
            "data": response_schema.dump(timetable)
        }), 201

    except ValueError as error:
        return jsonify({
            "message": str(error)
        }), 400

    except Exception as error:
        return jsonify({
            "message": "Failed to create timetable",
            "error": str(error)
        }), 500

# GET ALL TIMETABLES
@timetable_bp.route("/timetable", methods=["GET"])
@jwt_required()
@role_require("PRINCIPAL", "TEACHER")
def get_all_timetables():
    try:
        timetables = TimetableService.get_all_timetables()

        return jsonify({
            "message": "Timetables fetched successfully",
            "data": response_many_schema.dump(timetables)
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Failed to fetch timetables",
            "error": str(error)
        }), 500

# GET TIMETABLE BY ID
@timetable_bp.route("/timetable/<int:timetable_id>", methods=["GET"])
@jwt_required()
@role_require("PRINCIPAL", "TEACHER")
def get_timetable_by_id(timetable_id):
    try:
        timetable = TimetableService.get_timetable_by_id(
            timetable_id
        )

        if not timetable:
            return jsonify({
                "message": "Timetable not found"
            }), 404

        return jsonify({
            "message": "Timetable fetched successfully",
            "data": response_schema.dump(timetable)
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Failed to fetch timetable",
            "error": str(error)
        }), 500

# GET TIMETABLE BY CLASS ID
@timetable_bp.route("/timetable/class/<int:class_id>", methods=["GET"])
@jwt_required()
@role_require("PRINCIPAL", "TEACHER")
def get_timetable_by_class(class_id):
    try:
        timetables = TimetableService.get_by_class_id(class_id)

        return jsonify({
            "message": "Class timetable fetched successfully",
            "data": response_many_schema.dump(timetables)
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Failed to fetch class timetable",
            "error": str(error)
        }), 500

# GET TIMETABLE BY SUBJECT ID
@timetable_bp.route("/timetable/subject/<int:subject_id>", methods=["GET"])
@jwt_required()
@role_require("PRINCIPAL", "TEACHER")
def get_timetable_by_subject(subject_id):
    try:
        timetables = TimetableService.get_by_subject_id(subject_id)

        return jsonify({
            "message": "Subject timetable fetched successfully",
            "data": response_many_schema.dump(timetables)
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Failed to fetch subject timetable",
            "error": str(error)
        }), 500


# GET TIMETABLE BY TEACHER ID
@timetable_bp.route("/teacher/<int:teacher_id>", methods=["GET"])
@jwt_required()
@role_require("PRINCIPAL", "TEACHER")
def get_timetable_by_teacher(teacher_id):
    try:
        timetables = TimetableService.get_by_teacher_id(teacher_id)

        return jsonify({
            "message": "Teacher timetable fetched successfully",
            "data": response_many_schema.dump(timetables)
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Failed to fetch teacher timetable",
            "error": str(error)
        }), 500

# GET TIMETABLE BY DAY
@timetable_bp.route("/day/timetable/<string:day_of_week>", methods=["GET"])
@jwt_required()
@role_require("PRINCIPAL", "TEACHER")
def get_timetable_by_day(day_of_week):
    try:
        timetables = TimetableService.get_by_day(day_of_week)

        return jsonify({
            "message": "Day-wise timetable fetched successfully",
            "data": response_many_schema.dump(timetables)
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Failed to fetch day-wise timetable",
            "error": str(error)
        }), 500

# UPDATE TIMETABLE
@timetable_bp.route("/update/timetable/<int:timetable_id>", methods=["PUT"])
@jwt_required()
@role_require("PRINCIPAL")
def update_timetable(timetable_id):
    data = request.get_json()

    errors = update_schema.validate(data)

    if errors:
        return jsonify({
            "message": "Validation failed",
            "errors": errors
        }), 400

    try:
        updated_timetable = TimetableService.update_timetable(
            timetable_id,
            data
        )

        if not updated_timetable:
            return jsonify({
                "message": "Timetable not found"
            }), 404

        return jsonify({
            "message": "Timetable updated successfully",
            "data": response_schema.dump(updated_timetable)
        }), 200

    except ValueError as error:
        return jsonify({
            "message": str(error)
        }), 400

    except Exception as error:
        return jsonify({
            "message": "Failed to update timetable",
            "error": str(error)
        }), 500

# DELETE TIMETABLE
@timetable_bp.route("/delete/timetable/<int:timetable_id>", methods=["DELETE"])
@jwt_required()
@role_require("PRINCIPAL")
def delete_timetable(timetable_id):
    try:
        deleted = TimetableService.delete_timetable(
            timetable_id
        )

        if not deleted:
            return jsonify({
                "message": "Timetable not found"
            }), 404

        return jsonify({
            "message": "Timetable deleted successfully"
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Failed to delete timetable",
            "error": str(error)
        }), 500