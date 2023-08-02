import pytest
import requests
import os


@pytest.fixture(scope="session")
def jwt_token():
    # token = get_token()
    token = os.environ.get("TOKEN")
    return token


def get_token() -> str:
    url = "https://thegrapefruitsduo.us.auth0.com/oauth/token"

    payload = {
        "client_id": "WQrIbh4gPU7ypcMKxxQA18eBGCOGfNxH",
        "client_secret": "yoDuOx7My5L9A-qqS5bZIICglfzrwUn_DLkS5BjasdI0shFHP-sMKytDBcpDKRsY",
        "audience": "https://api.thegrapefruitsduo.com",
        "grant_type": "client_credentials",
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)
    token = response.json().get("access_token")
    if token is None:
        raise Exception("token is none")
    return token
