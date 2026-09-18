from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from school.services.auth_services import AuthServices
from school.services.user_services import UserServices
from school.utils.role_decorator import role_require

from school.Schema.user_schema import (
    UserCreateSchema,
    UserLoginSchema,
    UserResponseSchema
)


user_bp = Blueprint(
    "users",
    __name__
)


user_create_schema = UserCreateSchema()
user_login_schema = UserLoginSchema()
user_response_schema = UserResponseSchema(
    many=True
)


#REGISTER USERS
@user_bp.route("/user/register", methods=["POST"])
def register_user():
    data = request.get_json()

    errors = UserCreateSchema().validate(data)

    if errors:
        return jsonify({
            "message": "Validation failed",
            "errors": errors
        }), 400

    try:
        user = AuthServices.create_user(data)

        return jsonify({
            "message": "User registered successfully",
            "user": UserResponseSchema().dump(user)
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


#LOGIN USER
@user_bp.route("/user/login", methods=["POST"])
def login_user():
    data = request.get_json()

    errors = UserLoginSchema().validate(data)

    if errors:
        return jsonify({
            "message": "Validation failed",
            "errors": errors
        }), 400

    try:
        token = AuthServices.login(data)

        return jsonify({
            "message": "Login successful",
            "access_token": token
        }), 200

    except ValueError as error:
        return jsonify({
            "message": str(error)
        }), 401

    except Exception as error:
        return jsonify({
            "message": "Something went wrong",
            "error": str(error)
        }), 500


#GET CURRENT USER PROFILE
@user_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_my_profile():
    current_user_id = get_jwt_identity()

    try:
        user = UserServices.get_user_by_id(int(current_user_id))

        if not user:
            return jsonify({
                "message": "User not found"
            }), 404

        return jsonify({
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "phone_number": user.phone_number,
            "date_of_birth": user.date_of_birth,
            "role": user.role,
            "login_date": user.login_date
        }), 200

    except ValueError:
        return jsonify({
            "message": "User not found"
        }), 404

    except Exception as error:
        return jsonify({
            "message": "Something went wrong",
            "error": str(error)
        }), 500

#GET ALL USERS
@user_bp.route("all_users/profile", methods=["GET"])
@jwt_required()
@role_require("PRINCIPAL")
def get_all_users():
    try:
        users = UserServices.get_all_user()

        return jsonify({
            "message": "Users fetched successfully",
            "users": user_response_schema.dump(users)
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Something went wrong",
            "error": str(error)
        }), 500

#GET USER BY ID
@user_bp.route("/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user_by_id(user_id):
    current_user_id = int(get_jwt_identity())
    claims = get_jwt()
    current_role = claims.get("role")

    if current_role != "PRINCIPAL" and current_user_id != user_id:
        return jsonify({
            "message": "You can access only your own profile"
        }), 403

    try:
        user = UserServices.get_user_by_id(user_id)

        if not user:
            return jsonify({
                "message": "User not found"
            }), 404

        return jsonify({
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "phone_number": user.phone_number,
            "date_of_birth": user.date_of_birth,
            "role": user.role,
            "login_date": user.login_date
        }), 200

    except ValueError:
        return jsonify({
            "message": "User not found"
        }), 404

    except Exception as error:
        return jsonify({
            "message": "Something went wrong",
            "error": str(error)
        }), 500

#UPDATE USERS
@user_bp.route("/<int:user_id>", methods=["PUT"])
@jwt_required()
def update_user(user_id):
    current_user_id = int(get_jwt_identity())
    claims = get_jwt()
    current_role = claims.get("role")

    if current_role != "PRINCIPAL" and current_user_id != user_id:
        return jsonify({
            "message": "You can update only your own profile"
        }), 403

    data = request.get_json()

    try:
        user = UserServices.update_user(user_id, data)

        if not user:
            return jsonify({
                "message": "User not found"
            }), 404

        return jsonify({
            "message": "User updated successfully",
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "phone_number": user.phone_number,
                "date_of_birth": user.date_of_birth,
                "role": user.role
            }
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


#DELETE USERS
@user_bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
@role_require("PRINCIPAL")
def delete_user(user_id):
    try:
        deleted = UserServices.delete_user(user_id)

        if not deleted:
            return jsonify({
                "message": "User not found"
            }), 404

        return jsonify({
            "message": "User deleted successfully"
        }), 200

    except ValueError:
        return jsonify({
            "message": "User not found"
        }), 404

    except Exception as error:
        return jsonify({
            "message": "Something went wrong",
            "error": str(error)
        }), 500