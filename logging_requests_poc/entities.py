"""ENTITIES
Data models used on the application
"""

# # Native # #
from typing import List

# # Installed # #
import pydantic

__all__ = ("UserCreate", "User", "Users")


class UserCreate(pydantic.BaseModel):
    username: str


class User(UserCreate):
    user_id: str


Users = List[User]
