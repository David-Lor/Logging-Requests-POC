"""TEST - CREATE
"""

# # Native # #
import json

# # Installed # #
import requests
from ward import test

# # Package # #
from tests.utils import *


@test("should create the user and return it")
def _(db=database_fixture):
    body = get_user_create()

    response = requests.post("http://localhost:5000/users", json=body, headers=headers)
    response.raise_for_status()
    response_body = json.loads(response.text)

    assert response.status_code == 201
    assert response_body["username"] == body["username"]
    assert isinstance(response_body["user_id"], str)


@test("should return 500 when creating an user with \"fail\" on the username")
def _(db=database_fixture):
    body = {
        "username": "must fail"
    }

    response = requests.post("http://localhost:5000/users", json=body, headers=headers)

    assert response.status_code == 500
