"""TEST - FIND ONE (GET ONE)
"""

# # Native # #
import json
import random
from uuid import uuid4

# # Installed # #
import requests
from ward import test

# # Package # #
from tests.utils import *


@test("should get all the existing users")
def _(db=database_fixture):
    existing_users = [get_existing_user() for _ in range(3)]
    user = random.choice(existing_users)

    response = requests.get(f"http://localhost:5000/users/{user.user_id}")
    response.raise_for_status()
    response_body = json.loads(response.text)

    assert response.status_code == 200
    assert response_body == user.dict()


@test("should return 404 when user does not exist")
def _(db=database_fixture):
    response = requests.get(f"http://localhost:5000/users/{uuid4()}")

    assert response.status_code == 404
