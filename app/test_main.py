import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    res = client.get("/")
    assert res.status_code == 200
    assert isinstance(res.json(), dict)
    assert "msg" in res.json()
    assert res.json().get("msg") == "The Grapefruits Duo API"


def test_protected(jwt_token):
    headers = {"authorization": f"Bearer {jwt_token}"}
    res = client.get("/api/private", headers=headers)
    assert res.status_code == 200

    headers = {"authorization": f"Bearer INVALIDJWT"}
    res = client.get("/api/private", headers=headers)
    print(res.json())
    print(res.status_code)
    assert res.status_code == 400

    res = client.get("/api/private")
    assert res.status_code == 403


def test_nonexistant():
    res = client.get("/asdfasdfqg")
    assert res.status_code == 404
    assert res.json() == {"detail": "Not Found"}
