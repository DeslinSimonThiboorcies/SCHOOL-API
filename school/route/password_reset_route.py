from flask import Blueprint, request, jsonify

from school.services.password_reset_service import PasswordResetService


password_reset_bp = Blueprint(
    "password_reset",
    __name__,
    url_prefix="/api/auth"
)


@password_reset_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json()

    account_type = data.get("account_type") if data else None
    email = data.get("email") if data else None

    if not account_type or not email:
        return jsonify({
            "message": "account_type and email are required"
        }), 400

    account_type = account_type.upper().strip()
    if account_type not in ["STUDENT", "TEACHER", "PRINCIPAL"]:
        return jsonify({
            "message": "account_type must be STUDENT, TEACHER or PRINCIPAL"
        }), 400

    try:
        result = PasswordResetService.create_reset_token(
            account_type,
            email
        )

        return jsonify({
            "message": result["message"],
            "reset_url": result["reset_url"],
            "expires_at": result["expires_at"]
        }), 200

    except ValueError as error:
        return jsonify({
            "message": str(error)
        }), 404 if str(error) == "Account not found" else 400

    except Exception as error:
        return jsonify({
            "message": "Failed to process password reset request",
            "error": str(error)
        }), 500


@password_reset_bp.route("/verify-reset-token", methods=["POST"])
def verify_reset_token():
    data = request.get_json()

    token = data.get("token") if data else None
    account_type = data.get("account_type") if data else None

    if not token or not account_type:
        return jsonify({
            "message": "token and account_type are required"
        }), 400

    try:
        PasswordResetService.verify_reset_token(token, account_type)
        return jsonify({
            "message": "Reset token is valid"
        }), 200
    except ValueError as error:
        return jsonify({
            "message": str(error)
        }), 400


@password_reset_bp.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json()

    token = data.get("token") if data else None
    account_type = data.get("account_type") if data else None
    new_password = data.get("new_password") if data else None

    if not token or not account_type or not new_password:
        return jsonify({
            "message": "token, account_type and new_password are required"
        }), 400

    if len(new_password) < 8:
        return jsonify({
            "message": "Password must contain at least 8 characters"
        }), 400

    try:
        result = PasswordResetService.reset_password(
            token,
            account_type,
            new_password
        )

        return jsonify({
            "message": result["message"]
        }), 200

    except ValueError as error:
        return jsonify({
            "message": str(error)
        }), 400

    except Exception as error:
        return jsonify({
            "message": "Failed to reset password",
            "error": str(error)
        }), 500