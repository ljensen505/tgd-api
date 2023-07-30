from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    res = client.get("/")
    assert res.status_code == 200
    assert isinstance(res.json(), dict)
    assert "msg" in res.json()
    assert res.json().get("msg") == "The Grapefruits Duo API"


def test_nonexistant():
    res = client.get("/asdfasdfqg")
    assert res.status_code == 404
    assert res.json() == {"detail": "Not Found"}
