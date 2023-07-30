from fastapi.testclient import TestClient
from app.main import app
from random import randint

client = TestClient(app)


def test_events():
    res = client.get("/events")
    assert res.status_code == 200
    assert isinstance(res.json(), dict)
    assert len(res.json()) >= 3
    for id in res.json():
        event = res.json().get(id)
        assert len(event) == 7
        assert isinstance(event.get("id"), int)
        assert isinstance(event.get("name"), str)


def test_event():
    for id in [1, 2, 3]:
        res = client.get(f"/events/{id}")
        assert res.status_code == 200
        assert isinstance(res.json(), dict)
        assert len(res.json()) == 7
        for attr in [
            "name",
            "id",
            "description",
            "image_url",
            "location",
            "date",
            "ticket_url",
        ]:
            assert attr in res.json()

    for id in [randint(10, 100) for _ in range(25)]:
        res = client.get(f"/events/{id}")
        assert res.status_code == 404
