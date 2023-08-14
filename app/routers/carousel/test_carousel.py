from fastapi.testclient import TestClient
from app.main import app
import requests

client = TestClient(app)


def test_images():
    res = client.get("/carousel")
    assert res.status_code == 200
    assert isinstance(res.json(), dict)
    assert len(res.json()) >= 2
    for id in res.json():
        img = res.json().get(id)
        assert len(img) == 2
        assert isinstance(img.get("id"), str)
        assert isinstance(img.get("url"), str)


def test_image():
    img_ids = [
        "livingroom_bz0pp6",
        "wLTu18p_byqaov",
        "MandCthumbnail_image0-DELedit_copy_jdtngw",
        "studio_esvm3n",
    ]
    for img_id in img_ids:
        print(img_id)
        res = client.get(f"/carousel/{img_id}")
        assert res.status_code == 200
        url = res.json().get("url")
        assert url is not None
        assert res.json().get("id") is not None
        cloudinary_res = requests.get(url)
        assert cloudinary_res.status_code == 200
        assert cloudinary_res.headers.get("Content-Type") == "image/jpeg"


def test_del(jwt_token):
    img_id = "livingroom_bz0pp6"

    # no token
    res = client.delete(f"/carousel/{img_id}")
    assert res.status_code == 403

    # test for invalid jwt
    headers = {"authorization": "Bearer notAJWT"}
    res = client.delete(f"/carousel/{img_id}", headers=headers)
    assert res.status_code == 400
    assert isinstance(res.json().get("detail"), str)

    # valid jwt but bad image id
    headers = {"authorization": f"Bearer {jwt_token}"}
    res = client.delete(f"/carousel/123abc", headers=headers)
    assert res.status_code == 404
    assert res.json().get("detail") == "image not found"

    # valid delete requests are verified in test_post


def test_post(jwt_token):
    # no jwt
    res = client.post("/carousel")
    assert res.status_code == 403

    # invalid jwt and no image (422 due to no image)
    headers = {"authorization": "Bearer notAJWT"}
    res = client.post(f"/carousel", headers=headers)
    assert res.status_code == 422

    with open("imgs/IMG_4845.jpg", "rb") as file_obj:
        headers = {"authorization": f"Bearer {jwt_token}"}
        res = client.post("/carousel", headers=headers, files={"file": file_obj})

    assert res.status_code == 201
    img_id = res.json().get("id")
    img_url = res.json().get("url")
    assert None not in [img_id, img_url]

    cloud_res = requests.get(img_url)
    assert cloud_res.status_code == 200
    assert cloud_res.headers.get("Content-Type") == "image/jpeg"

    res = client.delete(f"/carousel/{img_id}", headers=headers)
    assert res.status_code == 204

    res = client.get("/carousel")
    assert img_id not in res.json()


def test_invalid(jwt_token):
    bad_imgs = ["pdf-test.pdf", "proj06-b.cpp"]
    for img in bad_imgs:
        with open(f"imgs/{img}", "rb") as image_file:
            headers = {"authorization": f"Bearer {jwt_token}"}
            response = client.post(
                "/carousel", headers=headers, files={"file": image_file}
            )
        assert response.status_code == 400


def test_jpeg(jwt_token):
    headers = {"authorization": f"Bearer {jwt_token}"}
    with open("imgs/carol.jpeg", "rb") as image_file:
        response = client.post("/carousel", headers=headers, files={"file": image_file})
    assert response.status_code == 201
    img_id = response.json().get("id")

    client.delete(f"/carousel/{img_id}", headers=headers)
