from flask import jsonify
from functools import wraps
from flask_jwt_extended import get_jwt_identity
from school.repositories.teacher_repo import TeacherRepository

def school_principl(func):

    @wraps(func)
    def decoratore(*args, **kwargs):

        students_id = int(get_jwt_identity())
        principle = TeacherRepository.view_teacher(students_id)

        if principle.role not in ["PRINCIPAL", "TEACHER"]:
            return jsonify({
                "Message" : "Access Denied!"
            }), 403

        return func(*args, **kwargs)
    return decoratore