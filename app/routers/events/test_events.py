from fastapi.testclient import TestClient
from app.main import app
from random import randint
import requests

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


def test_post_and_del(jwt_token):
    headers = {"authorization": f"Bearer {jwt_token}"}
    payload = {
        "name": "My New Event",
        "date": "2023-08-17T20:59:19.157Z",
        "description": "A clever description here",
        "image_url": "https://thegrapefruitsduo.com/static/images/events/jazz-station.jpg",
        "location": "Some address here",
    }
    res = client.post("/events", headers=headers, json=payload)
    assert res.status_code == 201
    event_id = res.json().get("id")
    image_url = res.json().get("image_url")
    attrs = ["id", "name", "date", "description", "location"]
    for attr in attrs:
        assert attr in res.json()

    assert client.get(f"/events/{event_id}").status_code == 200
    assert requests.get(image_url)

    # delete image
    res = client.delete(f"/events/{event_id}", headers=headers)
    assert res.status_code == 204
    assert client.get(f"/events/{event_id}").status_code == 404
    assert str(event_id) not in client.get("/events").json()
