import pytest
import requests
import os


@pytest.fixture(scope="session")
def jwt_token():
    token = get_token()
    # token = os.environ.get("TOKEN")
    return token


def get_token() -> str:
    url = "https://thegrapefruitsduo.us.auth0.com/oauth/token"

    payload = {
        "client_id": os.environ.get("CLIENT_ID"),
        "client_secret": os.environ.get("CLIENT_SECRET"),
        "audience": "https://api.thegrapefruitsduo.com",
        "grant_type": "client_credentials",
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)
    token = response.json().get("access_token")
    if token is None:
        raise Exception("token is none")
    return token
