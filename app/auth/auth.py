import os
from fastapi import HTTPException, status
from fastapi.testclient import TestClient
import jwt


def set_up():
    """Sets up configuration for the app"""
    config = {
        "DOMAIN": os.getenv("AUTH0_DOMAIN"),
        "API_AUDIENCE": os.getenv("AUTH0_AUDIENCE"),
        "ISSUER": os.getenv("AUTH0_ISSUER"),
        "ALGORITHMS": os.getenv("ALGORITHMS"),
    }
    return config


class VerifyToken:
    """Does all the token verification using PyJWT"""

    def __init__(self, token):
        from app.main import app

        self.token = token
        self.config = set_up()
        self.client = TestClient(app)

        # This gets the JWKS from a given URL and does processing so you can
        # use any of the keys available
        jwks_url = f'https://{self.config["DOMAIN"]}/.well-known/jwks.json'
        self.jwks_client = jwt.PyJWKClient(jwks_url)

    def verify(self):
        err = None
        # This gets the 'kid' from the passed token
        try:
            self.signing_key = self.jwks_client.get_signing_key_from_jwt(self.token).key
        except jwt.exceptions.PyJWKClientError as error:
            err = {"status": "error", "msg": error.__str__()}
        except jwt.exceptions.DecodeError as error:
            err = {"status": "error", "msg": error.__str__()}

        if err:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=err.get("msg")
            )

        try:
            payload = jwt.decode(
                self.token,
                self.signing_key,
                algorithms=self.config["ALGORITHMS"],  # type: ignore
                audience=self.config["API_AUDIENCE"],
                issuer=self.config["ISSUER"],
            )
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

        if payload.get("status"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=payload.get("msg")
            )

        sub = payload.get("sub")
        users = self.client.get("/users").json()

        if sub not in users:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="not authorized"
            )

        # pprint(payload)

        return payload
