"""SETTINGS HANDLER
Load settings from .env or variable environment
"""

# # Installed # #
from dotenv_settings_handler import BaseSettingsHandler
from dotenv import load_dotenv

__all__ = ("api_settings", "mongo_settings")


class ApiSettings(BaseSettingsHandler):
    host = "0.0.0.0"
    port = 5000

    class Config:
        env_prefix = "API_"


class MongoSettings(BaseSettingsHandler):
    uri = "mongodb://127.0.0.1:27017"
    database = "logging-requests-poc"
    collection_users = "users"
    collection_logs = "logs"

    class Config:
        env_previx = "MONGO_"


load_dotenv()
api_settings = ApiSettings()
mongo_settings = MongoSettings()
