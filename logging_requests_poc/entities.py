"""ENTITIES
Data models used on the application
"""

# # Native # #
from typing import List

# # Installed # #
import pydantic

__all__ = ("UserCreate", "User", "Users")


class UserCreate(pydantic.BaseModel):
    """User Create object, part of POST requests body
    """
    username: str


class User(UserCreate):
    """User whole object, part of API responses and read/write on database
    """
    user_id: str


Users = List[User]
