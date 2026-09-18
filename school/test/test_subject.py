SUBJECTS_URL = "/api/subjects"


def test_create_subject_requires_authentication(client):
    response = client.post("/api/subjects/register/subject/", json={})
    assert response.status_code == 401


def test_create_subject_requires_principal(client, teacher_headers):
    response = client.post(
        "/api/subjects/register/subject/",
        json={
            "subject_name": "Mathematics",
            "subject_code": "MATH-101",
            "description": "Core mathematics",
        },
        headers=teacher_headers,
    )
    assert response.status_code == 403


def test_teacher_can_list_subjects(client, teacher_headers):
    response = client.get(
        "/api/subjects/view_all_subject/",
        headers=teacher_headers,
    )
    assert response.status_code == 200
    assert response.get_json()["subjects"] == []
