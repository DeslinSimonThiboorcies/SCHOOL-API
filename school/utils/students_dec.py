from functools import wraps

from flask import jsonify
from flask_jwt_extended import (
    verify_jwt_in_request,
    get_jwt_identity
)

from school.repositories.students_repo import StudentRepository
from school.models.users import User


def student_access_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()

        current_user_id = int(get_jwt_identity())

        student_id = kwargs.get("student_id")

        if student_id is None:
            student_id = kwargs.get("id")

        student = StudentRepository.get_by_id(student_id)

        if not student:
            return jsonify({
                "message": "Student not found"
            }), 404

        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({
                "message": "User not found"
            }), 404

        if (
            current_user.role not in {"PRINCIPAL", "TEACHER"}
            and student.user_id != current_user_id
        ):
            return jsonify({
                "message": "You do not have permission to access this student"
            }), 403

        return function(*args, **kwargs)

    return wrapper