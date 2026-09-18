from school.test.conftest import auth_headers


ATTENDANCE_URL = "/api/student/attendance"


def test_create_attendance_requires_authentication(client):
    response = client.post(ATTENDANCE_URL, json={})
    assert response.status_code == 401


def test_create_attendance_rejects_invalid_payload(client, principal_headers):
    response = client.post(
        ATTENDANCE_URL,
        json={"student_id": 1},
        headers=principal_headers,
    )
    assert response.status_code == 400
    assert response.get_json()["message"] == "Validation failed"


def test_teacher_can_read_attendance(client, teacher_headers):
    response = client.get(
        "/api/student/attendance/",
        headers=teacher_headers,
    )
    assert response.status_code == 200
    assert response.get_json()["data"] == []
