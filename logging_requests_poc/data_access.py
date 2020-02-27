"""DATA ACCESS
Functions to perform CRUD operations on entities
"""

# # Native # #
from uuid import uuid1

# # Package # #
from logging_requests_poc.database import mongo_users
from logging_requests_poc.entities import User, Users, UserCreate
from logging_requests_poc.exceptions import NotFoundError
from logging_requests_poc.logger import requests_logger as logger


class UsersDataAccess:
    @staticmethod
    def list() -> Users:
        entities = list(mongo_users.find())
        logger.debug(f"Read {len(entities)} entities from DB: {entities}")
        
        parsed_entities = [User(**entity) for entity in entities]
        logger.debug(f"Parsed entities from DB: {entities}")
        
        return parsed_entities

    @staticmethod
    def get_by_user_id(user_id: str) -> User:
        logger.debug(f"Searching entity in DB with user id {user_id}")
        entity = mongo_users.find_one({"user_id": user_id})

        if not entity:
            logger.debug(f"No entity found with user id {user_id}")
            raise NotFoundError(user_id)
        else:
            parsed_entity = User(**entity)
            logger.debug(f"Parsed entity: {parsed_entity}")
            return parsed_entity

    @staticmethod
    def get_by_document_id(document_id: str) -> User:
        logger.debug(f"Searching entity in DB with document id {document_id}")
        entity = mongo_users.find_one({"_id": document_id})

        if not entity:
            logger.debug(f"No entity found with document id {document_id}")
            raise NotFoundError(document_id)
        else:
            parsed_entity = User(**entity)
            logger.debug(f"Parsed entity: {parsed_entity}")
            return parsed_entity

    @staticmethod
    def post(user_create: UserCreate) -> User:
        entity = User(
            **user_create.dict(),
            user_id=str(uuid1())
        ).dict()
        logger.debug(f"Inserting new entity in DB: {entity}")

        if "fail" in user_create.username.lower():
            raise ValueError("The username contains the word \"fail\"")

        if "warn" in user_create.username.lower():
            logger.warning("The username contains 'warn'")

        inserted_id = mongo_users.insert_one(entity).inserted_id
        logger.info(f"Inserted entity with document id {inserted_id} in DB")

        return UsersDataAccess.get_by_document_id(inserted_id)

    @staticmethod
    def delete_by_user_id(user_id: str):
        logger.debug(f"Deleting entity from DB with user id {user_id}")
        entity = mongo_users.find_one_and_delete({"user_id": user_id})

        if not entity:
            logger.debug(f"No entity found with user id {user_id}")
            raise NotFoundError(user_id)
        else:
            logger.info(f"""Deleted entity with document id {entity["_id"]}""")
