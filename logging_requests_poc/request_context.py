"""REQUEST CONTEXT
Context Manager that must be used on any request, to handle errors and logging
"""

# # Native # #
import uuid
import contextlib
from typing import Optional

# # Package # #
from logging_requests_poc.error_handler import manage_endpoint_exceptions
from logging_requests_poc.logger import requests_logger as logger


@contextlib.contextmanager
def contextualize_request(request_verb: str, request_id: Optional[str] = None):
    if not request_id:
        request_id = str(uuid.uuid4())
    
    with logger.contextualize(request_id=request_id, request_verb=request_verb):
        with manage_endpoint_exceptions():
            logger.info("Request started")
            yield
            with logger.contextualize(last_request=True):
                logger.debug("Request completed successfully")
