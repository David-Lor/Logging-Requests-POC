"""TEST - LIST (GET ALL)
"""

# # Native # #
import json

# # Installed # #
import requests
from ward import test

# # Package # #
from tests.utils import *


@test("should get all the existing users")
def _(db=database_fixture):
    existing_users = [get_existing_user() for _ in range(3)]

    response = requests.get("http://localhost:5000/users")
    response.raise_for_status()
    response_body = json.loads(response.text)

    assert response.status_code == 200
    assert isinstance(response_body, list)
    assert len(response_body) == len(existing_users)
    assert response_body == existing_users
