from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from school.services.fee_service import FeeService
from school.Schema.fee_schema import (
    FeeCreateSchema,
    FeeUpdateSchema,
    FeeResponseSchema
)
from school.utils.role_decorator import role_require


fee_bp = Blueprint(
    "fees",
    __name__,
    url_prefix="/api/fees"
)


create_schema = FeeCreateSchema()
update_schema = FeeUpdateSchema()
response_schema = FeeResponseSchema()
response_many_schema = FeeResponseSchema(many=True)


# --------------------------------------------------
# CREATE FEE
# --------------------------------------------------

@fee_bp.route("/", methods=["POST"])
@jwt_required()
@role_require("PRINCIPAL")
def create_fee():
    data = request.get_json()

    errors = create_schema.validate(data)

    if errors:
        return jsonify({
            "message": "Validation failed",
            "errors": errors
        }), 400

    try:
        fee = FeeService.create_fee(data)

        return jsonify({
            "message": "Fee record created successfully",
            "data": response_schema.dump(fee)
        }), 201

    except ValueError as error:
        return jsonify({
            "message": str(error)
        }), 400

    except Exception as error:
        return jsonify({
            "message": "Failed to create fee record",
            "error": str(error)
        }), 500


# --------------------------------------------------
# GET ALL FEES
# --------------------------------------------------

@fee_bp.route("/", methods=["GET"])
@jwt_required()
@role_require("PRINCIPAL", "TEACHER")
def get_all_fees():
    try:
        fees = FeeService.get_all_fees()

        return jsonify({
            "message": "Fee records fetched successfully",
            "data": response_many_schema.dump(fees)
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Failed to fetch fee records",
            "error": str(error)
        }), 500


# --------------------------------------------------
# GET FEE BY ID
# --------------------------------------------------

@fee_bp.route("/<int:fee_id>", methods=["GET"])
@jwt_required()
@role_require("PRINCIPAL", "TEACHER")
def get_fee_by_id(fee_id):
    try:
        fee = FeeService.get_fee_by_id(fee_id)

        if not fee:
            return jsonify({
                "message": "Fee record not found"
            }), 404

        return jsonify({
            "message": "Fee record fetched successfully",
            "data": response_schema.dump(fee)
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Failed to fetch fee record",
            "error": str(error)
        }), 500


# --------------------------------------------------
# GET FEES BY STUDENT ID
# --------------------------------------------------

@fee_bp.route("/student/<int:student_id>", methods=["GET"])
@jwt_required()
@role_require("PRINCIPAL", "TEACHER")
def get_fees_by_student(student_id):
    try:
        fees = FeeService.get_by_student_id(student_id)

        return jsonify({
            "message": "Student fee records fetched successfully",
            "data": response_many_schema.dump(fees)
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Failed to fetch student fee records",
            "error": str(error)
        }), 500


# --------------------------------------------------
# GET FEES BY PAYMENT STATUS
# --------------------------------------------------

@fee_bp.route("/status/<string:payment_status>", methods=["GET"])
@jwt_required()
@role_require("PRINCIPAL", "TEACHER")
def get_fees_by_status(payment_status):
    try:
        fees = FeeService.get_by_payment_status(payment_status)

        return jsonify({
            "message": "Fee records fetched by payment status",
            "data": response_many_schema.dump(fees)
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Failed to fetch fee records by status",
            "error": str(error)
        }), 500


# --------------------------------------------------
# UPDATE FEE
# --------------------------------------------------

@fee_bp.route("/<int:fee_id>", methods=["PUT"])
@jwt_required()
@role_require("PRINCIPAL")
def update_fee(fee_id):
    data = request.get_json()

    errors = update_schema.validate(data)

    if errors:
        return jsonify({
            "message": "Validation failed",
            "errors": errors
        }), 400

    try:
        updated_fee = FeeService.update_fee(
            fee_id,
            data
        )

        if not updated_fee:
            return jsonify({
                "message": "Fee record not found"
            }), 404

        return jsonify({
            "message": "Fee record updated successfully",
            "data": response_schema.dump(updated_fee)
        }), 200

    except ValueError as error:
        return jsonify({
            "message": str(error)
        }), 400

    except Exception as error:
        return jsonify({
            "message": "Failed to update fee record",
            "error": str(error)
        }), 500


# --------------------------------------------------
# DELETE FEE
# --------------------------------------------------

@fee_bp.route("/<int:fee_id>", methods=["DELETE"])
@jwt_required()
@role_require("PRINCIPAL")
def delete_fee(fee_id):
    try:
        deleted = FeeService.delete_fee(fee_id)

        if not deleted:
            return jsonify({
                "message": "Fee record not found"
            }), 404

        return jsonify({
            "message": "Fee record deleted successfully"
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Failed to delete fee record",
            "error": str(error)
        }), 500