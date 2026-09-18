MARKS_URL = "/api/students/marks"


def test_create_mark_requires_authentication(client):
    response = client.post(MARKS_URL, json={})
    assert response.status_code == 401


def test_create_mark_validates_payload(client, principal_headers):
    response = client.post(
        MARKS_URL,
        json={"student_id": 1, "subject_id": 1},
        headers=principal_headers,
    )
    assert response.status_code == 400
    assert response.get_json()["message"] == "Validation failed"


def test_teacher_can_list_marks(client, teacher_headers):
    response = client.get(MARKS_URL, headers=teacher_headers)
    assert response.status_code == 200
    assert response.get_json()["data"] == []
