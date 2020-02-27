"""SETTINGS HANDLER
Load settings from .env or variable environment
"""

# # Installed # #
from pydantic import BaseSettings

__all__ = ("api_settings", "mongo_settings")


class ApiSettings(BaseSettings):
    host = "0.0.0.0"
    port = 5000
    persist_log_level = "ERROR"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.persist_log_level = self.persist_log_level.strip().upper()

    class Config:
        env_prefix = "API_"
        env_file = ".env"


class MongoSettings(BaseSettings):
    uri = "mongodb://127.0.0.1:27017"
    database = "logging-requests-poc"
    collection_users = "users"
    collection_logs = "logs"

    class Config:
        env_prefix = "MONGO_"
        env_file = ".env"


api_settings = ApiSettings()
mongo_settings = MongoSettings()
