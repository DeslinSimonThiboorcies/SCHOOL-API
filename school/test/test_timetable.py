TIMETABLE_URL = "/api/timetable"


def test_create_timetable_requires_authentication(client):
    response = client.post(TIMETABLE_URL, json={})
    assert response.status_code == 401


def test_create_timetable_requires_principal(client, teacher_headers):
    response = client.post(
        TIMETABLE_URL,
        json={
            "class_id": 1,
            "subject_id": 1,
            "teacher_id": 1,
            "day_of_week": "MONDAY",
            "start_time": "09:00:00",
            "end_time": "10:00:00",
            "room_number": "A-101",
        },
        headers=teacher_headers,
    )
    assert response.status_code == 403


def test_teacher_can_list_timetables(client, teacher_headers):
    response = client.get(TIMETABLE_URL, headers=teacher_headers)
    assert response.status_code == 200
    assert response.get_json()["data"] == []
