from functools import wraps

from flask import jsonify
from flask_jwt_extended import (
    verify_jwt_in_request,
    get_jwt_identity
)

from school.repositories.teacher_repo import TeacherRepository
from school.models.users import User


def teacher_access_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()

        current_user_id = int(get_jwt_identity())

        teacher_id = kwargs.get("teacher_id")

        if teacher_id is None:
            teacher_id = kwargs.get("id")

        teacher = TeacherRepository.get_by_id(teacher_id)

        if not teacher:
            return jsonify({
                "message": "Teacher not found"
            }), 404

        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({
                "message": "User not found"
            }), 404

        if (
            current_user.role != "PRINCIPAL"
            and teacher.user_id != current_user_id
        ):
            return jsonify({
                "message": "You do not have permission to access this teacher"
            }), 403

        return function(*args, **kwargs)

    return wrapper