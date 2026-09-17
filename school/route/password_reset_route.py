from flask import Blueprint, request, jsonify
from school.services.password_reset_service import PasswordResetService

password_reset_bp = Blueprint(
    "password_reset",
    __name__
)

@password_reset_bp.route(
    "/auth/forgot-password",
    methods=["POST"]
)
def forgot_password():

    data = request.get_json() or {}
    account_type = data.get("account_type")
    email = data.get("email")

    if not account_type or not email:
        return jsonify({
            "message": "account_type and email are required"
        }), 400

    account_type = account_type.upper().strip()
    email = email.lower().strip()

    if account_type not in [
        "STUDENT",
        "TEACHER",
        "PRINCIPAL"
    ]:
        return jsonify({
            "message": (
                "account_type must be STUDENT, TEACHER or PRINCIPAL"
            )
        }), 400

    try:

        result = PasswordResetService.create_reset_token(
            account_type=account_type,
            email=email
        )

        return jsonify(result), 200

    except ValueError as error:

        return jsonify({
            "message": str(error)
        }), 404

    except Exception as error:

        return jsonify({
            "message": "Something went wrong",
            "error": str(error)
        }), 500


@password_reset_bp.route(
    "/auth/verify-reset-token",
    methods=["POST"]
)
def verify_reset_token():

    data = request.get_json() or {}

    raw_token = data.get("token")
    account_type = data.get("account_type")

    if not raw_token or not account_type:
        return jsonify({
            "message": "token and account_type are required"
        }), 400

    account_type = account_type.upper().strip()

    try:

        PasswordResetService.verify_reset_token(
            raw_token=raw_token,
            account_type=account_type
        )

        return jsonify({
            "message": "Reset token is valid"
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


@password_reset_bp.route(
    "/auth/reset-password",
    methods=["POST"]
)
def reset_password():

    data = request.get_json() or {}

    raw_token = data.get("token")
    account_type = data.get("account_type")
    new_password = data.get("new_password")

    if not raw_token or not account_type or not new_password:
        return jsonify({
            "message": (
                "token, account_type and new_password are required"
            )
        }), 400

    account_type = account_type.upper().strip()

    try:

        result = PasswordResetService.reset_password(
            raw_token=raw_token,
            account_type=account_type,
            new_password=new_password
        )

        return jsonify(result), 200

    except ValueError as error:

        return jsonify({
            "message": str(error)
        }), 400

    except Exception as error:

        return jsonify({
            "message": "Something went wrong",
            "error": str(error)
        }), 500