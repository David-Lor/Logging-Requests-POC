"""TEST - FIND ONE (GET ONE)
"""

# # Native # #
from uuid import uuid4

# # Installed # #
import requests
from ward import test

# # Project # #
from logging_requests_poc.database import mongo_users

# # Package # #
from tests.utils import *


@test("should delete an existing user")
def _(db=database_fixture):
    user = get_existing_user()

    response = requests.delete(f"http://localhost:5000/users/{user.user_id}")
    response.raise_for_status()

    assert response.status_code == 200
    assert mongo_users.find_one({"user_id": user.user_id}) is None


@test("should return 404 when user does not exist")
def _(db=database_fixture):
    response = requests.delete(f"http://localhost:5000/users/{uuid4()}")

    assert response.status_code == 404
