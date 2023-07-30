from fastapi.testclient import TestClient
from app.main import app
from random import randint

client = TestClient(app)


def test_users():
    res = client.get("/users")
    assert res.status_code == 200
    assert isinstance(res.json(), dict)
    assert len(res.json()) >= 4
    for id in res.json():
        user = res.json().get(id)
        assert len(user) == 2
        assert isinstance(user.get("id"), str)
        assert isinstance(user.get("name"), str)


def test_user():
    user_ids = [
        "google-oauth2|103593642272149633528",
        "google-oauth2|109109812131608294748",
        "google-oauth2|110044702811943457315",
        "google-oauth2|116470512398914344676",
    ]
    for id in user_ids:
        res = client.get(f"/users/{id}")
        assert res.status_code == 200
        assert isinstance(res.json(), dict)
        for attr in ["name", "id"]:
            assert attr in res.json()
            assert len(res.json()) == 2

    for id in [randint(1, 100) for _ in range(100)]:
        res = client.get(f"/users/{id}")
        assert res.status_code == 404

    invalid_ids = [
        f"google-oauth2|{randint(100_000_000_000_000_000_000, 200_000_000_000_000_000_000)}"
        for _ in range(100)
    ]
    for id in [invalid_ids]:
        res = client.get(f"/users/{id}")
        assert res.status_code == 404


def test_methods():
    res = client.post("/users")
    assert res.status_code == 405

    res = client.put("/users")
    assert res.status_code == 405

    res = client.delete("/users")
    assert res.status_code == 405
