"""ENTRYPOINT
Runner for the API; endpoint definition and initial request handlers
"""

# # Installed # #
import uvicorn

# # Package # #
from logging_requests_poc.app import app
from logging_requests_poc.settings_handler import api_settings
from logging_requests_poc.logger import system_logger as logger

__all__ = ("run",)


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
