FEES_URL = "/api/fees/"


def test_create_fee_requires_authentication(client):
    response = client.post(FEES_URL, json={})
    assert response.status_code == 401


def test_create_fee_requires_principal(client, teacher_headers):
    response = client.post(
        FEES_URL,
        json={
            "student_id": 1,
            "fee_type": "Tuition",
            "amount": 100.0,
            "due_date": "2026-10-01",
        },
        headers=teacher_headers,
    )
    assert response.status_code == 403


def test_teacher_can_list_fees(client, teacher_headers):
    response = client.get(FEES_URL, headers=teacher_headers)
    assert response.status_code == 200
    assert response.get_json()["data"] == []
