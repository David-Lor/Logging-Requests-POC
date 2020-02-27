"""ERROR HANDLER
Handler that translates Python exceptions into HTTP responses and logs errors
"""

# # Native # #
import contextlib
import traceback

# # Installed # #
import fastapi

# # Package # #
from logging_requests_poc.exceptions import NotFoundError
from logging_requests_poc.logger import requests_logger as logger

__all__ = ("manage_endpoint_exceptions",)


@contextlib.contextmanager
def manage_endpoint_exceptions():
    try:
        yield

    except NotFoundError as error:
        raise fastapi.HTTPException(
            status_code=404,
            detail=f"Resource {error.identifier} not found"
        )

    except Exception as error:
        # Set the last_request flag to the log record, so the log handler can send all the request records to MongoDB
        with logger.contextualize(last_request=True):
            logger.error(f"Error while handling request: {error}\n{traceback.format_exc()}")
        raise error  # re-raise so API can return 500
