from flask_jwt_extended import create_access_token
from school.test.conftest import auth_headers


def test_student_and_teacher_collision(
        app, 
        create_teacher, 
        create_student, 
        client
    ):

    create_teacher(
        name = "Real Principal", 
        email = "real.principal@example.com", 
        role = "PRINCIPAL"
    )

    student = create_student(
        name = "Just A Student", 
        email = "student.collide@example.com"
    )

    assert student.id == 1

    with app.app_context():
        student_token = create_access_token(
            identity=str(student.user_id),
            additional_claims={"role": "STUDENT"}
        )

    response = client.get(
        "/api/view/profile", 
        headers = auth_headers(student_token)
    )

    assert response.status_code == 403