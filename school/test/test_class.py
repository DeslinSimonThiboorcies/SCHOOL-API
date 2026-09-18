CLASS_URL = "/api/class/"


def test_create_class_requires_authentication(client):
    response = client.post("/api/class/register/", json={})
    assert response.status_code == 401


def test_create_class_requires_principal(client, teacher_headers):
    response = client.post(
        "/api/class/register/",
        json={
            "class_name": "Grade 1",
            "section": "A",
            "academic_year": "2026-2027",
        },
        headers=teacher_headers,
    )
    assert response.status_code == 403


def test_principal_can_list_classes(client, principal_headers):
    response = client.get(CLASS_URL, headers=principal_headers)
    assert response.status_code == 200
    assert response.get_json()["classes"] == []
