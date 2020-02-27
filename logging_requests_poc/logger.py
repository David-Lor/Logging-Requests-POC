"""LOGGER
Loggers used on the APP
"""

# # Native # #
import sys
import json

# # Installed # #
from loguru import logger

# # Project # #
from logging_requests_poc.database import mongo_logs
from logging_requests_poc.settings_handler import api_settings as settings

__all__ = ("system_logger", "requests_logger")

_request_records = dict()
"""Local cache for the request records organized by request id: { request_id: record[] }"""


class LoggerFilter:
    """Names of virtual loggers to filter log records by their type (using the 'logger_name' context field)
    """
    system = "system"
    requests = "requests"


def _set_filter(name: str):
    """Filter is used to filter loguru.logger by the logger type,
    allowing to create multiple 'virtual' loggers.
    'logger_name' is the key used on log record 'extra' fields to identify 
    the type of logger, thus used on logger.bind calls to fetch each virtual logger.
    """
    def record_filter(record):
        return record["extra"].get("logger_name") == name
    return record_filter


def _request_handler(record: str):
    """Handler for any Request record received.
    Records are stored on the "_request_records" local cache.
    When a record with the context tag "last_request"=True is received, all the cached request records are persisted
    on MongoDB if any of the records reach the ERROR log level.
    The handler must be registered using logger.add(... , serialize=True)
    """
    record = json.loads(record)["record"]

    # Store in local record cache
    request_id = record["extra"].get("request_id")
    if request_id:
        try:
            _request_records[request_id].append(record)
        except KeyError:
            _request_records[request_id] = [record]

        # If this was last request record, pop from cache and insert on Mongo if exceeds level
        if record["extra"].get("last_request"):
            records = _request_records.pop(request_id)

            # TODO Send records to system log?
            if any(rec for rec in records if rec["level"]["no"] >= logger.level(settings.persist_log_level).no):
                system_logger.debug(f"Inserting {len(records)} log records of request {request_id} on Mongo")
                # Using an async mongo client would be preferably

                # Insert one document per log record:
                # mongo_logs.insert_many(records)

                # Insert one document per request:
                mongo_logs.insert_one({
                    "_id": request_id,
                    "records": records
                })


# Adding handlers to the logger
# https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.add

logger.remove()  # must remove the default logger
logger.add(
    sys.stderr,
    filter=_set_filter(LoggerFilter.system),  # filter by extra context property "logger_name"
    level="DEBUG"
)
logger.add(
    _request_handler,
    filter=_set_filter(LoggerFilter.requests),  # filter by extra context property "logger_name"
    level="DEBUG",
    serialize=True  # the record is provided as a JSON string to the handler
)

# Create virtual loggers by binding the context property "logger_name" to each record
# Each virtual logger can then use this property as a filter (done above)

system_logger = logger.bind(logger_name=LoggerFilter.system)
requests_logger = logger.bind(logger_name=LoggerFilter.requests)
