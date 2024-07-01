from typing import Annotated, Union
import base64
from fastapi import FastAPI, Header, Request
from requests.auth import HTTPBasicAuth
import requests
import os

app = FastAPI()

LOCATION_URL = "http://location-app-charts.auth"
HYDRA_ADMIN = "http://hydra-public.auth:4444"
OAUTH2_TOKEN = f"{HYDRA_ADMIN}/oauth2/token"
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
CLIENT_ID = os.environ["CLIENT_ID"]


def exchange_token() -> str:
    payload = {"grant_type": "client_credentials", "scope": "offline_access location:read"}
    basic = HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    response = requests.request("POST", OAUTH2_TOKEN, data=payload, auth=basic)
    print(response)
    return response.json()["access_token"]


@app.get("/headers")
def hello(request: Request):
    return {"headers": request.headers}


@app.get("/hello")
def hello(request: Request):
    return {"Hello": "welcome"}


# remove this endpointget
@app.get(
    "/get_internal_token",
)
def get_internal_token(user_id: Annotated[str | None, Header()] = None):
    jwt = exchange_token()
    return {"internal-token":jwt}

@app.get(
    "/location",
)
def get_user_location(user_id: Annotated[str | None, Header()] = None):
    jwt = exchange_token()
    resp = requests.get(
        f"{LOCATION_URL}/user_location",
        headers={"Authorization": f"Bearer {jwt}"},
    )
    if resp.status_code == 200:
        return {"result": resp.json()}
    elif resp.status_code in [401, 403]:
        return {"result": "unauthorized"}
    return {"result": resp.text}
