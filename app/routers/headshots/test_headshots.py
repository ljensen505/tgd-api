from fastapi.testclient import TestClient
from app.main import app
import requests

client = TestClient(app)


def test_images():
    res = client.get("/headshots")
    assert res.status_code == 200
    assert isinstance(res.json(), dict)
    assert len(res.json()) >= 2
    for id in res.json():
        img = res.json().get(id)
        assert isinstance(img.get("id"), str)
        assert isinstance(img.get("url"), str)
        assert isinstance(img.get("musician_id"), int)

        m_id = img.get("musician_id")
        m_res = client.get(f"/musicians/{m_id}")
        assert m_res.status_code == 200


def test_post_delete(jwt_token):
    headers = {"authorization": f"Bearer {jwt_token}"}
    with open("imgs/carol.jpeg", "rb") as image_file:
        response = client.post(
            "/headshots/musicians/1", headers=headers, files={"file": image_file}
        )
    assert response.status_code == 201
    img_id = response.json().get("id")

    res = client.get("/headshots")
    assert res.status_code == 200
    headshots = res.json()
    assert img_id in headshots

    # delete newly added photo
    res = client.delete(f"/headshots/{img_id}", headers=headers)
    assert res.status_code == 204

    res = client.get(f"/headshots{img_id}")
    assert res.status_code == 404

    res = client.get("/headshots")
    assert img_id not in res.json()


def test_404():
    res = client.get("/headshots/abc123")
    assert res.status_code == 404
