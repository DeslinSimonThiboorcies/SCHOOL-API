from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from school.services.attendance_service import AttendanceService
from school.Schema.attendance_schema import (
    AttendanceCreateSchema,
    AttendanceUpdateSchema,
    AttendanceResponseSchema
)
from school.utils.role_decorator import role_require

attendance_bp = Blueprint(
    "attendance",
    __name__
)

create_schema = AttendanceCreateSchema()
update_schema = AttendanceUpdateSchema()
response_schema = AttendanceResponseSchema()
response_many_schema = AttendanceResponseSchema(many=True)

# CREATE ATTENDANCE
@attendance_bp.route("/student/attendance", methods=["POST"])
@jwt_required()
@role_require("PRINCIPAL", "TEACHER")
def create_attendance():
    data = request.get_json()

    errors = create_schema.validate(data)

    if errors:
        return jsonify({
            "message": "Validation failed",
            "errors": errors
        }), 400

    try:
        attendance = AttendanceService.create_attendance(data)

        return jsonify({
            "message": "Attendance marked successfully",
            "data": response_schema.dump(attendance)
        }), 201

    except ValueError as error:
        return jsonify({
            "message": str(error)
        }), 400

    except Exception as error:
        return jsonify({
            "message": "Failed to mark attendance",
            "error": str(error)
        }), 500

# GET ALL ATTENDANCE

@attendance_bp.route("/student/attendance/", methods=["GET"])
@jwt_required()
@role_require("PRINCIPAL", "TEACHER")
def get_all_attendance():
    try:
        attendance_records = AttendanceService.get_all_attendance()

        return jsonify({
            "message": "Attendance records fetched successfully",
            "data": response_many_schema.dump(attendance_records)
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Failed to fetch attendance records",
            "error": str(error)
        }), 500


# GET ATTENDANCE BY ID
@attendance_bp.route("/student/attendance/<int:attendance_id>", methods=["GET"])
@jwt_required()
@role_require("PRINCIPAL", "TEACHER")
def get_attendance_by_id(attendance_id):
    try:
        attendance = AttendanceService.get_attendance_by_id(
            attendance_id
        )

        if not attendance:
            return jsonify({
                "message": "Attendance record not found"
            }), 404

        return jsonify({
            "message": "Attendance record fetched successfully",
            "data": response_schema.dump(attendance)
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Failed to fetch attendance record",
            "error": str(error)
        }), 500

# GET ATTENDANCE BY STUDENT ID
@attendance_bp.route("/student/attendance/<int:student_id>", methods=["GET"])
@jwt_required()
@role_require("PRINCIPAL", "TEACHER")
def get_attendance_by_student(student_id):
    try:
        attendance_records = AttendanceService.get_by_student_id(
            student_id
        )

        return jsonify({
            "message": "Student attendance fetched successfully",
            "data": response_many_schema.dump(attendance_records)
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Failed to fetch student attendance",
            "error": str(error)
        }), 500

# GET ATTENDANCE BY CLASS ID
@attendance_bp.route("/class/attendance/<int:class_id>", methods=["GET"])
@jwt_required()
@role_require("PRINCIPAL", "TEACHER")
def get_attendance_by_class(class_id):
    try:
        attendance_records = AttendanceService.get_by_class_id(
            class_id
        )

        return jsonify({
            "message": "Class attendance fetched successfully",
            "data": response_many_schema.dump(attendance_records)
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Failed to fetch class attendance",
            "error": str(error)
        }), 500

# GET ATTENDANCE BY DATE
@attendance_bp.route("/date/attendance/<attendance_date>", methods=["GET"])
@jwt_required()
@role_require("PRINCIPAL", "TEACHER")
def get_attendance_by_date(attendance_date):
    try:
        attendance_records = AttendanceService.get_by_date(
            attendance_date
        )

        return jsonify({
            "message": "Date-wise attendance fetched successfully",
            "data": response_many_schema.dump(attendance_records)
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Failed to fetch date-wise attendance",
            "error": str(error)
        }), 500

# UPDATE ATTENDANCE
@attendance_bp.route("/update/student/attendance/<int:attendance_id>", methods=["PUT"])
@jwt_required()
@role_require("PRINCIPAL", "TEACHER")
def update_attendance(attendance_id):
    data = request.get_json()

    errors = update_schema.validate(data)

    if errors:
        return jsonify({
            "message": "Validation failed",
            "errors": errors
        }), 400

    try:
        updated_attendance = AttendanceService.update_attendance(
            attendance_id,
            data
        )

        if not updated_attendance:
            return jsonify({
                "message": "Attendance record not found"
            }), 404

        return jsonify({
            "message": "Attendance updated successfully",
            "data": response_schema.dump(updated_attendance)
        }), 200

    except ValueError as error:
        return jsonify({
            "message": str(error)
        }), 400

    except Exception as error:
        return jsonify({
            "message": "Failed to update attendance",
            "error": str(error)
        }), 500

# DELETE ATTENDANCE
@attendance_bp.route("/delete/student/attendance/<int:attendance_id>", methods=["DELETE"])
@jwt_required()
@role_require("PRINCIPAL")
def delete_attendance(attendance_id):
    try:
        deleted = AttendanceService.delete_attendance(
            attendance_id
        )

        if not deleted:
            return jsonify({
                "message": "Attendance record not found"
            }), 404

        return jsonify({
            "message": "Attendance deleted successfully"
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Failed to delete attendance",
            "error": str(error)
        }), 500