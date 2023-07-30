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
        res = client.get(f"/carousel/{img_id}")
        assert res.status_code == 200
        url = res.json().get("url")
        assert url is not None
        assert res.json().get("id") is not None
        cloudinary_res = requests.get(url)
        assert cloudinary_res.status_code == 200
        assert cloudinary_res.headers.get("Content-Type") == "image/jpeg"
