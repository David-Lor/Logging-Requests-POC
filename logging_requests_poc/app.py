"""APP
API initialization, endpoints and main Run entrypoint function
"""

# # Native # #
import json

# # Installed # #
import fastapi
import uvicorn

# # Package # #
from logging_requests_poc.request_context import contextualize_request
from logging_requests_poc.data_access import UsersDataAccess
from logging_requests_poc.responses import Responses
from logging_requests_poc.entities import User, UserCreate, Users
from logging_requests_poc.settings_handler import api_settings
from logging_requests_poc.logger import system_logger as logger


__all__ = ("app",)

app = fastapi.FastAPI(
    title="Logging-Requests-POC",
    description="POC of request-based service with contextualized requests"
)


@app.get("/status")
async def endpoint_get_status():
    with contextualize_request("GET /status"):
        return Responses.ok()


@app.get("/users")
async def endpoint_list_users() -> Users:
    with contextualize_request("GET /users"):
        users = UsersDataAccess.list()
        return Responses.ok(json.dumps([user.dict() for user in users]))


@app.post("/users")
async def endpoint_post_user(user: UserCreate) -> User:
    with contextualize_request("POST /users"):
        created_user = UsersDataAccess.post(user)
        return Responses.created(created_user.json())


@app.get("/users/{user_id}")
async def endpoint_get_user(user_id: str) -> User:
    with contextualize_request(f"GET /users/{user_id}"):
        user = UsersDataAccess.get_by_user_id(user_id)
        return Responses.ok(user.json())


@app.delete("/users/{user_id}")
async def endpoint_delete_user(user_id: str):
    with contextualize_request(f"DELETE /users/{user_id}"):
        UsersDataAccess.delete_by_user_id(user_id)
        return Responses.ok(json.dumps({"deleted": True}))


# @app.patch("/users/{user_id}")
# async def endpoint_patch_user(user_id: str):
#     with contextualize_request():
#         pass


def run():
    """Run the API using Uvicorn
    """
    host = api_settings.host
    port = api_settings.port

    logger.info(f"Running API on {host}:{port}")
    uvicorn.run(
        app=app,
        host=host,
        port=port,
        # TODO combine uvicorn log with system log?
        log_level=1000  # disable uvicorn logs
    )
