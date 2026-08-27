from flask import jsonify
from functools import wraps
from flask_jwt_extended import get_jwt_identity
from school.repositories.teacher_repo import TeacherRepository

def principle(func):

    @wraps(func)
    def teacher_deco(*args, **kwargs):

        teacher_id = int(get_jwt_identity())
        currunt_teacher = TeacherRepository.view_teacher(teacher_id)

        if not currunt_teacher or currunt_teacher.role != "PRINCIPAL":
            return jsonify({
                "MESSAGE" : "ACCESS DENIED!"
            }), 403
        
        return func(*args, **kwargs)
    return teacher_deco