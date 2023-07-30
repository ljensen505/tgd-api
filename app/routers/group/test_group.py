from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_group():
    res = client.get("/group")
    assert res.status_code == 200
    assert isinstance(res.json(), dict)
    assert len(res.json()) >= 2
    assert res.json().get("name") == "The Grapefruits Duo"
    bio = res.json().get("bio")
    assert isinstance(bio, str)
    assert len(bio) > 0


def test_put():
    new_bio = "A new bio here"
    old_bio = "The Grapefruits, comprising of Coco Bender, piano, and Margarite Waddell, french horn, are a contemporary classical music duo. They perform frequently through out the PNW with the goal presenting traditional classical french horn repertoire, new 20th century works, and commissioned works by PNW composers. Our upcoming concert series features works by Jane Vignery, Tara Islas, Gliere, Prokofiev, and Oregon Composers Christina Rusnak and Mark Jacobs."

    err_payload = {"name": "not the grapefruits duo", "bio": "a suitable bio"}
    res = client.put("/group", json=err_payload)
    assert res.status_code == 400
    assert res.json() == {
        "detail": "Group name either missing or malformed. You cannot change the group name"
    }

    payload = {"name": "The Grapefruits Duo", "bio": new_bio}
    res = client.put("/group", json=payload)
    assert res.status_code == 200
    assert res.json().get("name") == "The Grapefruits Duo"
    assert res.json().get("bio") == new_bio

    payload = {"name": "The Grapefruits Duo", "bio": old_bio}
    res = client.put("/group", json=payload)
    assert res.status_code == 200
    assert res.json().get("name") == "The Grapefruits Duo"
    assert res.json().get("bio") == old_bio


def test_methods():
    res = client.post("/group")
    assert res.status_code == 405

    res = client.delete("/group")
    assert res.status_code == 405
