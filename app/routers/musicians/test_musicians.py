from fastapi.testclient import TestClient
from app.main import app
from random import randint

client = TestClient(app)


def test_musicians():
    res = client.get("/musicians")
    assert res.status_code == 200
    assert isinstance(res.json(), dict)
    assert len(res.json()) == 2
    coco = res.json().get("1")
    margarite = res.json().get("2")
    for m in [coco, margarite]:
        attrs = "name", "bio", "headshot"
        assert all([attr in m for attr in attrs])
    assert coco.get("name") == "Coco Bender"
    assert margarite.get("name") == "Margarite Waddell"


def test_musician():
    for id in [1, 2]:
        res = client.get(f"/musicians/{id}")
        assert res.status_code == 200
        assert isinstance(res.json(), dict)
        for attr in ["name", "bio", "headshot"]:
            assert attr in res.json()


def test_not_found():
    for _ in range(10):
        res = client.get(f"/musicians/{randint(3, 100)}")
        assert res.status_code == 404
        assert res.json().get("detail") == "No musician with that id was found"


def test_methods():
    res = client.post("/musicians")
    assert res.status_code == 405

    res = client.put("/musicians")
    assert res.status_code == 405

    res = client.delete("/musicians")
    assert res.status_code == 405
