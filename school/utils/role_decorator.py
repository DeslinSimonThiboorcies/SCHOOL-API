from functools import wraps

from flask import jsonify
from flask_jwt_extended import (
    verify_jwt_in_request,
    get_jwt
)


def role_require(*allowed_roles):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()

            claims = get_jwt()
            current_role = claims.get("role")

            if current_role not in allowed_roles:
                return jsonify({
                    "message": "You do not have permission to access this resource"
                }), 403

            return function(*args, **kwargs)

        return wrapper

    return decorator