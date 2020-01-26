"""DATABASE
MongoDB Database to persist both API data and log records
"""

# # Native # #
from pymongo import MongoClient

# # Project # #
from logging_requests_poc.settings_handler import mongo_settings as settings

__all__ = ("mongo", "mongo_database", "mongo_logs", "mongo_users")


class MongoDB(MongoClient):
    """Custom class to inject Mongo settings.
    Would be interesting to add logging to mongo methods
    """
    def __init__(self, *args, **kwargs):
        super().__init__(settings.uri, *args, **kwargs)


mongo = MongoDB()
mongo_database = mongo[settings.database]

mongo_users = mongo_database[settings.collection_users]
mongo_logs = mongo_database[settings.collection_logs]
