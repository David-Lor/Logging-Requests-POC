"""TEST - UTILS
"""

# # Native # #
import random

# # Installed # #
from ward import fixture

# # Project # #
from logging_requests_poc.entities import UserCreate
from logging_requests_poc.data_access import UsersDataAccess
from logging_requests_poc.database import mongo_users

__all__ = ("headers", "get_user_create", "get_existing_user", "database_fixture")

headers = {"Content-Type": "application/json"}


def _get_username():
    return f"Testing Agent {random.randint(1, 100)}"


@fixture
def database_fixture():
    """Delete all entries on users database after the test
    """
    yield mongo_users
    mongo_users.delete_many({})


def get_user_create():
    return {
        "username": _get_username()
    }


def get_existing_user():
    return UsersDataAccess.post(UserCreate(username=_get_username()))
