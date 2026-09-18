from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from school.services.class_service import ClassService

from school.Schema.class_schema import (
    ClassCreateSchema,
    ClassUpdateSchema,
    ClassResponseSchema
)

from school.utils.role_decorator import role_require


class_bp = Blueprint(
    "classes",
    __name__
)


class_create_schema = ClassCreateSchema()
class_update_schema = ClassUpdateSchema()
class_response_schema = ClassResponseSchema()
class_response_many_schema = ClassResponseSchema(many=True)


@class_bp.route("/class/register/", methods=["POST"])
@jwt_required()
@role_require("PRINCIPAL")
def create_class():
    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request body is required"
        }), 400

    errors = class_create_schema.validate(data)

    if errors:
        return jsonify({
            "message": "Validation failed",
            "errors": errors
        }), 400

    try:
        class_data = ClassService.create_class(data)

        return jsonify({
            "message": "Class created successfully",
            "class": class_response_schema.dump(class_data)
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


@class_bp.route("/class/", methods=["GET"])
@jwt_required()
@role_require("PRINCIPAL", "TEACHER")
def get_all_classes():
    try:
        classes = ClassService.get_all_classes()

        return jsonify({
            "message": "Classes fetched successfully",
            "classes": class_response_many_schema.dump(classes)
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Something went wrong",
            "error": str(error)
        }), 500


@class_bp.route("/view_class/<int:class_id>", methods=["GET"])
@jwt_required()
@role_require("PRINCIPAL", "TEACHER")
def get_class_by_id(class_id):
    try:
        class_data = ClassService.get_class_by_id(class_id)

        if not class_data:
            return jsonify({
                "message": "Class not found"
            }), 404

        return jsonify({
            "message": "Class fetched successfully",
            "class": class_response_schema.dump(class_data)
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Something went wrong",
            "error": str(error)
        }), 500


@class_bp.route("/class/update/<int:class_id>", methods=["PUT"])
@jwt_required()
@role_require("PRINCIPAL")
def update_class(class_id):
    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request body is required"
        }), 400

    errors = class_update_schema.validate(data)

    if errors:
        return jsonify({
            "message": "Validation failed",
            "errors": errors
        }), 400

    try:
        class_data = ClassService.update_class(
            class_id,
            data
        )

        if not class_data:
            return jsonify({
                "message": "Class not found"
            }), 404

        return jsonify({
            "message": "Class updated successfully",
            "class": class_response_schema.dump(class_data)
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


@class_bp.route("/class/delete/<int:class_id>", methods=["DELETE"])
@jwt_required()
@role_require("PRINCIPAL")
def delete_class(class_id):
    try:
        deleted = ClassService.delete_class(class_id)

        if not deleted:
            return jsonify({
                "message": "Class not found"
            }), 404

        return jsonify({
            "message": "Class deleted successfully"
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