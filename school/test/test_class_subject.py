CLASS_SUBJECT_URL = "/api/class/subjects"


def test_create_class_subject_requires_authentication(client):
    response = client.post(CLASS_SUBJECT_URL, json={})
    assert response.status_code == 401


def test_create_class_subject_validates_payload(client, principal_headers):
    response = client.post(
        CLASS_SUBJECT_URL,
        json={"class_id": 1},
        headers=principal_headers,
    )
    assert response.status_code == 400
    assert response.get_json()["message"] == "Validation failed"


def test_teacher_can_list_class_subjects(client, teacher_headers):
    response = client.get(
        "/api/class/subject",
        headers=teacher_headers,
    )
    assert response.status_code == 200
    assert response.get_json()["data"] == []
