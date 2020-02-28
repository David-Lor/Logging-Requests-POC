"""TEST - LOG PERSISTENCE
Verify that logs for failed requests are persisted on MongoDB
"""

# # Native # #
from uuid import uuid4

# # Installed # #
import requests
from ward import test
from pymongo.collection import Collection

# # Package # #
from tests.utils import *


@test("should store one document in MongoDB for the failed request")
def _(db: Collection = database_logs_fixture):
    body = {
        "username": "must fail"
    }

    response = requests.post("http://localhost:5000/users", json=body, headers=headers)
    assert response.status_code == 500

    documents = list(db.find({}))
    assert len(documents) == 1

    document = documents[0]

    # _id should be an uuid (check string length)
    assert len(document["_id"]) == len(str(uuid4()))

    # records should be an array
    assert isinstance(document["records"], list)

    # last record should be the ERROR record from the "error_handler" module
    last_record = document["records"][-1]
    assert last_record["level"]["name"] == "ERROR"
    assert last_record["module"] == "error_handler"


@test("should store one document in MongoDB for the warning request")
def _(db: Collection = database_logs_fixture):
    body = {
        "username": "must raise a warning"
    }

    response = requests.post("http://localhost:5000/users", json=body, headers=headers)
    assert response.status_code == 201

    documents = list(db.find({}))
    assert len(documents) == 1

    document = documents[0]

    # _id should be an uuid (check string length)
    assert len(document["_id"]) == len(str(uuid4()))

    # records should be an array
    assert isinstance(document["records"], list)

    # one of the records should have a level of WARNING
    assert any(
        record for record in document["records"]
        if record["level"]["name"] == "WARNING"
    )
